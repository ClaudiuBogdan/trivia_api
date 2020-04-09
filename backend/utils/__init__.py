def format_categories(categories):
    result_list = []
    for category in categories:
        result_list.append(category.format())
    return result_list


def format_questions(questions):
    result_list = []
    for question in questions:
        result_list.append(question.format())
    return result_list
