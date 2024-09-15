from flask import request, jsonify
from app.blueprints.webhook import webhook_bp
from mysql.connector import Error
from app.lib.twilio_utils import send_whatsapp_message
from app.lib import User, UserQuestionStage,Questions,ProfessionCounter,UserQuestionAnswers
from app.lib import is_integer,check_answer_in_range,check_eligiblity

@webhook_bp.route('/receive', methods=['POST'])
def receive_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    if request.values.get('MediaUrl0'):
        incoming_msg = request.values.get('MediaUrl0')
    user_from = request.values.get('WaId')

    #send_whatsapp_message(user_from,question[3])
    user = User().get_user_id(user_from)

    #if user doesn't exist in the database add them and add the stage to start
    if not user:
        user_id =User().add_user(user_from)
        if user_id:
            UserQuestionStage().add_question_stage(user_id,'engagement1')
            question = Questions().get_next_question('engagement1')
            send_whatsapp_message(user_from,question[3])
        question_stage = UserQuestionStage().get_user_question_stage(user_id)
        question = Questions().get_question(question_stage[0])
    else:
        user_id = user[0]
        question_stage = UserQuestionStage().get_user_question_stage(user_id)
        question = Questions().get_question(question_stage[0])
        if question_stage[0] not in ['question13','question21','question24','question32','question36','question19','question34','question45-1']:
            if not is_integer(incoming_msg):
                new_question = Questions().get_question('question45')
                send_whatsapp_message(user_from,new_question[3]) 
                return jsonify({'status': 'success'}), 200
            
        if question_stage[0] == 'question44':
            new_question = Questions().get_question('question49')
            send_whatsapp_message(user_from,new_question[3])
            return jsonify({'status': 'success'}), 200
               
        if question_stage[0] == 'question45-1':
            counter = UserQuestionAnswers().get_question_answer('question3',user_id)
            if int(counter[0]) == 3 or int(counter[0]) == 4 or int(incoming_msg) == 2 or int(incoming_msg) == 1:
                ProfessionCounter().update_profession_counter(int(counter[0]))

        if question_stage[0] == 'question3':
            if int(incoming_msg) == 3 or int(incoming_msg) == 4 or int(incoming_msg) == 2 or int(incoming_msg) == 1:
                counter = ProfessionCounter().get_profession_counter(int(incoming_msg))
                print(counter)
                if counter[0] >= counter[1]:
                    send_question = Questions().get_question('question45')
                    UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':incoming_msg })
                    print(send_question)
                    send_whatsapp_message(user_from,send_question[3])
                    return jsonify({'status': 'success'}), 200
            else:
                send_question = Questions().get_question('question48')
                UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':incoming_msg })
                send_whatsapp_message(user_from,send_question[3])
                return jsonify({'status': 'success'}), 200
            
                       
        if question_stage[0] == 'question8':
           if UserQuestionAnswers().literacy_check(user_id,['question6','question5','question8','question7'],incoming_msg) == False:
                UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':incoming_msg })
                new_question = Questions().get_question('question48')
                UserQuestionStage().add_question_stage(user_id,new_question[1])
                send_whatsapp_message(user_from,new_question[3])
                return jsonify({'status': 'success'}), 200
        is_sent = handle_question(user_id,question_stage,incoming_msg,question,user_from)
        if is_sent:
            return jsonify({'status': 'success'}), 200

        if question:
           answer_range = question[7]
           eligibity = question[6]
           is_eligible = check_eligiblity(incoming_msg,eligibity,question)
           is_in_range = check_answer_in_range(incoming_msg,answer_range)
           if is_in_range == False and question[1] != 'question3':
                new_question = Questions().get_question('question45')
                send_whatsapp_message(user_from,new_question[3])
                return jsonify({'status': 'success'}), 200
           if is_eligible and is_in_range:
                UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':incoming_msg })
                new_question = Questions().get_question(question[4])
                UserQuestionStage().add_question_stage(user_id,new_question[1])
                send_whatsapp_message(user_from,new_question[3])
           else:
                new_question = Questions().get_question('question48')
                UserQuestionStage().add_question_stage(user_id,new_question[1])
                UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':incoming_msg })
                send_whatsapp_message(user_from,new_question[3])
    # Return a response
    return jsonify({'status': 'success'}), 200

def question_switch(user_id,next_question,answer,question,user_from):
    if int(answer) != 1:
        UserQuestionAnswers().insert_user_question_answer({'user_id':user_id,'question_id':question[0],'answer':answer })
        new_question = Questions().get_question(next_question)
        UserQuestionStage().add_question_stage(user_id,new_question[1])
        send_whatsapp_message(user_from,new_question[3])
        return True
    return False          

def handle_question(user_id, question_stage, incoming_msg, question, user_from):
    question_map = {
        'question12': 'question15',
        'question18': 'question21',
        'question23': 'question26',
        'question31': 'question34',
        'question35': 'question42'
    }
    current_question = question_stage[0]
    if current_question == 'question27':
        if int(incoming_msg) == 4:
            UserQuestionAnswers().insert_user_question_answer({'user_id': user_id, 'question_id': question[0], 'answer': incoming_msg})
            new_question =Questions().get_question('question31')
            UserQuestionStage().add_question_stage(user_id, new_question[1])
            send_whatsapp_message(user_from, new_question[3])
            return True
    elif current_question in question_map:
        next_question = question_map[current_question]
        switch_result = question_switch(user_id, next_question, incoming_msg, question, user_from)
        if switch_result:
            return True
    else:
        print('Last case')
