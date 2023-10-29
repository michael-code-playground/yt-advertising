def sort_videos(option):
    #sorting videos parameters
    if option == 1:
        ordered_by = ['videoCount', 'relevance', 'rating', 'viewCount']
    elif option == 2:
        ordered_by = ['date','rating', 'viewCount','relevance',]
    return ordered_by
        
def set_properties(option):
    #set right properties to chosen category
    if option == 1:
        keywords = "learn english|english vocabulary|English teacher|ielts|English vocabulary|study english|English learning grammar|English tips|speak english|English language|English grammar|ingles learning|learning english|English class toefl|learn English online|esl education|aprender ingles|idioms|learn language| English course|English online|English lesson|phrasal verbs"
        sub_count_limit = 40000
        upper_limit = None
        category = (keywords,sub_count_limit, upper_limit)
    elif option == 2:
        keywords ="fitness|sport|news|games|crypto|music"
        sub_count_limit = 700
        upper_limit = 10000
        category = (keywords,sub_count_limit, upper_limit)    
    return category