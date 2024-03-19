
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "No current question found."

    if not answer:
        return False, "Please provide a valid answer."

    session[current_question_id] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0


    try:
        current_question_index = PYTHON_QUESTION_LIST.index(current_question_id)
    except ValueError:
        return PYTHON_QUESTION_LIST[0], 0

    if current_question_index + 1 < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[current_question_index + 1], current_question_index + 1
    else:
        return None, -1


def generate_final_response(session):
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for question_id, correct_answer in enumerate(PYTHON_QUESTION_LIST):
        user_answer = session.get(str(question_id))
        if user_answer == correct_answer:
            correct_answers += 1

    score_percentage = (correct_answers / total_questions) * 100

    if score_percentage >= 70:
        final_response = f"Congratulations! You have successfully completed the quiz with a score of {score_percentage}%."
    else:
        final_response = f"Thank you for taking the quiz. Your score is {score_percentage}%. You can try again to improve your knowledge."

    return final_response
