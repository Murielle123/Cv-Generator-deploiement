def check_competences(json):
    if type(json['Compétences']) is list:
        json['Compétences'] = json['Compétences'][0]
        for competence in json['Compétences']:
            competence_values = json['Compétences'][competence]
            if type(competence_values) is list:
                json['Compétences'][competence] = ', '.join(competence_values)
    return json

def check_langues(json):
    if type(json['Langues']) is list:
        json['Langues'] = json['Langues'][0]
    return json

def check_keys(json):
    # Formater les champs defectueux
    for key in json:
        value = json[key]
        if type(value) is list:
            value = value[0]
        if type(value) is dict:
            for subkey in list(value): 
                # Toutes les sorties d'erreurs possibles doivent être mis dans cette liste.
                if subkey in ['nom entreprise']:
                   corrected_key =  "nom de l'entreprise"
                   value[corrected_key] = value[subkey]
                   del value[subkey]
                if subkey in ['nom poste']:
                    corrected_key =  "nom du poste occupé"
                    value[corrected_key] = value[subkey]
                    del value[subkey]   
    return json

def json_checker(json):
    
    check_competences(json)
    check_langues(json)
    check_keys(json)
    
    return json

# json_langues = {
#     'Langues': [{'Arabe': 'Courant', 'Anglais': 'Courant'}]
#     }

# json_competences = {'Compétences': [{
#         'Langages': ['Python', 'Java'],
#         'Logiciels': 'Word, Excel'
# }]}

# json_keys = {
#     'Formations':{
#         'nom entreprise': 'ENTREPRISE',
#         'nom poste': 'POSTE'
#     }
# }


# print('Avant: ', json_keys)
# print('Après: ', check_keys(json_keys))
