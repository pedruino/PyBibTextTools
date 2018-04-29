import os
from pybtex.database import parse_file
from pybtex.database import BibliographyData, Entry
import unidecode

folder = 'C:/Users/marcelo/Google Drive/Doutorado/Revisão Sistematica (1)/resultados pesquisas/'

pesquisas = [{'lib':'Scholar','filename':'G.Scholar.bib'},
             {'lib':'ACM','filename':'ACM.bib'},
             {'lib':'IEEE','filename':'IEEE.bib'},
             {'lib':'Scopus','filename':'scopus.bib'},
             {'lib':'Elsevier','filename':'ScienceDirect.bib'}]

bigFinal = BibliographyData()

mesclados = 0 
def mergeEntry(original, novo):
    global mesclados
    mesclado = False

    year1 = int(original.fields['year'])
    year2 = int(novo.fields['year'])
    if (year2>year1):
        original.fields['year'] = novo.fields['year']
        mesclado = True

    for novoKey in novo.fields.keys():
        if novoKey not in original.fields.keys():
            original.fields[novoKey] = novo.fields[novoKey]
            mesclado = True

    abs1 = ""
    abs2 = ""
    if "abstract" in original.fields.keys():
        abs1 = original.fields['abstract']
    if "abstract" in novo.fields.keys():
        abs2 = novo.fields['abstract']
    if (len(abs2)>len(abs1)):
        original.fields['abstract'] = novo.fields['abstract']
        mesclado = True

    if (mesclado):
        mesclados = mesclados + 1

    return original



i = 0
semAutor = 0
semAno = 0 
semJornal = 0
duplicados = 0
for pesquisa in pesquisas:

    bib_data = parse_file(os.path.join(folder,pesquisa['filename']))

    for entry in bib_data.entries.values():
        i = i + 1

        if not 'author' in entry.persons.keys():
            semAutor = semAutor + 1
        elif not 'year' in entry.fields.keys() or int(entry.fields['year'])==0:
            semAno = semAno + 1
        elif (not 'journal' in entry.fields.keys() ) and (not 'booktitle' in entry.fields.keys() ):
            semJornal = semJornal + 1
        else:                
            #print(entry.key)
            #print(entry.persons.keys())
            #print(entry.fields.keys())
            #print(entry.persons['author'])
            #print(entry.fields['title'])
            key =  entry.key.lower()

            entry.fields['note'] = pesquisa['lib']
            entryVelho = None

            cc = 0
            for entry1 in bigFinal.entries.values():
                if (entry1.fields['title'].lower()==entry.fields['title'].lower()):
                    year = int(entry.fields['year'])
                    year1 = int(entry1.fields['year'])
                    diff = abs(year-year1)
                    if (diff==0):
                        #if (cc>0):
                        #    print("==== Encontrou ", cc)
                        entryVelho = entry1
                    elif (diff==1 or diff==2):
                        lastname = unidecode.unidecode(entry.persons['author'][0].last_names[0]).lower()
                        lastname1 = unidecode.unidecode(entry1.persons['author'][0].last_names[0]).lower()
                        first_name = unidecode.unidecode(entry.persons['author'][0].first_names[0]).lower()
                        first_name1 = unidecode.unidecode(entry1.persons['author'][0].first_names[0]).lower()

                        if (lastname==lastname1 or lastname==first_name1 or lastname1==first_name):
                            #if (cc>0):
                            #    print("==== Encontrou ", cc)
                            entryVelho = entry1
                        else:
                            cc = cc + 1    
                            #print("====", cc)
                            #print(entry1.fields['title'])
                            #print(year,year1)
                            #print(entry1.persons['author'])
                            #print(entry.persons['author'])
  
            if (entryVelho != None):
                duplicados = duplicados + 1
                bigFinal.entries[entryVelho.key] = mergeEntry(entryVelho, entry)

            else:
                while (key in bigFinal.entries.keys()):
                    key = key +"_a"
                bigFinal.entries[key] = entry
            #print(i , len(bigFinal.entries), entry.key, key)

    
    #print(bib_data.to_string('bibtex'))
    #bib_data.to_file() 

#print(bigFinal.to_string('bibtex'))
print("Total ", i)

print("Sem autor ", semAutor)
print("Sem Ano ", semAno)
print("Sem Jornal ", semJornal)


print("Duplicados ", duplicados, " mesclados ",mesclados)
print("Final ", len(bigFinal.entries))
#print(bigFinal.entries.keys())

#print(bigFinal.entries[bigFinal.entries.keys()[0]] )




    


