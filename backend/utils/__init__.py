from models import Category


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


def format_categories_from_questions(questions):
    categories_list = []
    result_list = []
    for question in questions:
        category_id = question['category']
        if category_id not in categories_list:
            categories_list.append(category_id)

    for category_id in categories_list:
        result_list.append(Category.query.get(category_id).format())
    return result_list
