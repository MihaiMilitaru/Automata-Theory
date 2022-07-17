# Echipa
# grupa 143
# Florea Madalin-Alexandru
# Besliu Radu-Stefan
# Militaru Mihai-Alexandru

from distutils.filelist import translate_pattern
import sys

# Pentru a rula: python 4.py config_4.txt ( sau config_4_2.txt ) input_4.txt

# Programul copiază inputul pe ambele benzi ( banda principală și cea de backup )
# La fiecare operație, modificările se efectuează în același timp pe ambele benzi
# Cand se ajunge în starea de accept, sunt comparate cele două benzi și se afișează un mesaj corespunzător

# „getSection”: funcție care returnează liniile unei anumite secțiuni în fișier de intrare
# este folosit pentru a separa secțiuni (stări, sigma, gamma, tranziții, stare de pornire, stare de acceptare, stare de respingere)
def getSection(name, configLines):
    flag = False
    section = []

    for line in configLines:
        if line == name + ":":  # începutul secțiunii
            flag = True
            continue
        if line == "end":  # sfârșitul secțiunii
            flag = False
        if flag == True and line not in section:  # dacă nu am ajuns la sfârșitul secțiunii, anexăm linia fișierui la listă
            section.append(line)

    return section


# „loadFromFile”: funcție care utilizează funcția „getSection”, pentru a încărca secțiunile unui fișier de configurare TM
# și returnați-le în liste, împreună cu un cod de eroare dacă fișier nu este valid
def loadFromFile(fileName):
    configLines = []
    errorCode = 0

    file = open(fileName)

    for line in file:
        line = line.strip().lower()
        if len(line) > 0 and line[0] != "#":  # creăm o listă din fișier de intrare numai cu
            configLines.append(line)                 # rânduri care sunt diferite de comentarii
                                              # astfel încât să-l putem trece la funcția „getSection”.

    states = list(getSection("states", configLines))  # obținerea stărilor TM 
    sigma = list(getSection("sigma", configLines))  # obținerea alfabetului de intrare al TM
    gamma = list(getSection("gamma", configLines))  # obținerea alfabetului de bandă al TM
    transitions = list(getSection("transitions", configLines))  # obținerea tranzițiilor TM
    startState = list(getSection("start state", configLines))  #obținerea stării de pornire a TM 
    acceptState = list(getSection("accept state", configLines))  # obținerea stării de acceptare a TM
    rejectState = list(getSection("reject state", configLines))  # obținerea stării de respingere a TM

    # dacă fișierul nu conține exact o stare de pornire, returnăm un cod de eroare
    if len(startState) != 1:
        errorCode = 5
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișierul nu conține exact o stare de acceptare, returnăm un cod de eroare
    if len(acceptState) != 1:
        errorCode = 6
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișier nu conține exact o stare de respingere, returnăm un cod de eroare
    if len(rejectState) != 1:
        errorCode = 7
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișier nu conține cel puțin trei stări, inclusiv starea de pornire, starea de acceptare și starea de respingere,
    #  returnăm un cod de eroare

    if len(states) < 3:
        errorCode = 1
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
    elif startState[0] not in states or acceptState[0] not in states or rejectState[0] not in states:
        errorCode = 1
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișierul conține simbolul gol ("_") în alfabetul de intrare sau dacă alfabetul de intrare
    # este gol, returnăm un cod de eroare
    if "_" in sigma or len(sigma) == 0:
        errorCode = 2
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișierul nu conține simbolul gol ("_") în alfabetul de bandă sau 
    # dacă alfabetul de intrare nu este inclus în alfabetul de bandă sau 
    # dacă alfabetul de bandă este gol, returnăm un cod de eroare
    if "_" not in gamma or len(set(gamma)) != len(set(gamma)|set(sigma)) or len(gamma) == 0:
        errorCode = 3
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    # dacă fișierul nu conține nicio tranziție, returnăm un cod de eroare
    if len(transitions) == 0:
        errorCode = 4
        return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
    else:
        for transition in transitions:
            transition = transition.split()
            print(transition)
            if len(transition) != 5: #dacă o tranziție nu conține exact 5 elemente, returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
            elif transition[0] not in states or transition[1] not in states:  #dacă primele două elemente ale unei tranziții nu sunt stări din fișier , returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
            elif transition[0] == acceptState[0] or transition[0] == rejectState[0]:  # dacă prima stare a unei tranziții este fie starea de acceptare, fie starea de respingere, returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
            elif transition[2] not in gamma:  # dacă al treilea element al unei tranziții nu este un simbol din alfabetul benzii, returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
            elif transition[3] not in gamma and transition[3] != "e":  # dacă al patrulea element al unei tranziții nu este un simbol din alfabetul benzii (excluzând epsilon), returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState
            elif transition[4] != "l" and transition[4] != "r":  # dacă direcția în care se va mișca în continuare capul nu este nici stânga, nici dreapta, returnăm un cod de eroare
                errorCode = 4
                return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState

    file.close()

    #dacă fișierul de configurare TM este valid, nu returnăm niciun cod de eroare
    return errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState


try:
    errorCode, states, sigma, gamma, transitions, startState, acceptState, rejectState = loadFromFile(sys.argv[1])

    print()
    if errorCode == 1:
        print(f"Sectiunea \"States\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 2:
        print(f"Sectiunea \"Sigma\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 3:
        print(f"Sectiunea \"Gamma\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 4:
        print(f"Sectiunea \"Transitions\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 5:
        print(f"Sectiunea \"Start state\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 6:
        print(f"Sectiunea \"Accept state\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    elif errorCode == 7:
        print(f"Sectiunea \"Reject state\" din fisierul \"{sys.argv[1]}\" nu este valida.")
    else:
        print(f"Fisierul \"{sys.argv[1]}\" este valid! Masina Turing acceptata!")
        print()

        inputTM = open(sys.argv[2])

        print(f"Se valideaza șirul de intrare de la \"{sys.argv[2]}\":")
        print("----------------------------------")
        for string in inputTM:
            # se creează cele două benzi
            # ambele benzi sunt modificate in același timp
            tape = list(string.rstrip("\n"))
            tape2 = list(string.rstrip("\n"))

            tape[0:0] = [startState[0]]
            tape2[0:0] = [startState[0]]

            position = 0  # ținem evidența poziției stării curente, pe bandă
            flag = 1  # folosim o variabilă pentru a ști când să oprim validarea unui șir
            equalTapes = False # variabilă pentru compararea benzilor

            while flag == 1:  # continuăm validarea șirurilor, atâta timp cât nu am ajuns la un punct final
                flag = 0  #îi spunem programului că încă nu a avut loc nicio tranziție

                for transition in transitions:  # cautam tranzitia care incepe cu starea curenta si citeste primul simbol situat in dreapta starii curente
                    transition = transition.split()
                    if (transition[0] == tape[position-1] or transition[0] == tape[position])  and transition[2] == tape[position + 1]:
                        print(tape, transition, position)
                        if transition[4] == "l":  # capul ar trebui să meargă la stânga
                            if position == 0:  # am ajuns deja la capătul din stânga casetei, adică nu mai putem merge la stânga
                                flag = 2       # astfel, îi spunem programului să încheie validarea șirurilor, deoarece nu vom putea trece de pătratul din stânga benzii.
                                break
                            else:
                                if transition[3] != "e":  # pe lângă schimbarea stării curente cu un simbol, înlocuim și valoarea simbolului cu una diferită
                                    tape[position - 1] = transition[1]
                                    tape[position] = transition[3]

                                    tape2[position - 1] = transition[1]
                                    tape2[position] = transition[3]
                                else:  # schimbăm starea curentă cu un simbol, fără a înlocui valoarea simbolului
                                    symbolAux = tape[position - 1]
                                    tape[position - 1] = transition[1]
                                    tape[position] = symbolAux
                                    
                                    symbolAux2 = tape2[position - 1]
                                    tape2[position - 1] = transition[1]
                                    tape2[position] = symbolAux2

                                position -= 1
                            flag = 1  # spunem programului că a avut loc o tranziție
                        else:  # capul ar trebui să meargă la dreapta
                            if position == (len(tape) - 2):  # dacă am ajuns la pătratul dinaintea celui mai din dreapta pătrat al benzii, adăugăm un simbol gol pe bandă
                                tape.append("_")
                                tape2.append("_")
                            if transition[3] != "e":  # pe lângă schimbarea stării curente cu un simbol, înlocuim și acest din urmă simbol cu ​​un simbol diferit
                                tape[position + 1] = transition[1]
                                tape[position] = transition[3]
                                
                                tape2[position + 1] = transition[1]
                                tape2[position] = transition[3]
                            else:  # schimbăm starea curentă cu un simbol, fără a înlocui valoarea simbolului
                                symbolAux = tape[position + 1]
                                tape[position + 1] = transition[1]
                                tape[position] = symbolAux
                                
                                symbolAux2 = tape2[position + 1]
                                tape2[position + 1] = transition[1]
                                tape2[position] = symbolAux2
                            position += 1
                            flag = 1  # spunem programului că a avut loc o tranziție

                # dacă una din benzi ajunge in starea de accept, atunci considerăm că TM acceptă acest input
                if tape[position] == acceptState[0] or tape2[position] == acceptState[0]:
                    flag = 3 # am ajuns în starea de acceptare și astfel încheiem validarea șirului

                    # se verică egalitatea benzilor
                    if tape == tape2:
                        equalTapes = True
                    
                elif tape[position] == rejectState[0]:
                    flag = 4  # am ajuns în starea de respingere și astfel încheiem validarea șirului

            string = string.strip("\n")

            if flag == 3:
                print(f'Sirul "{string}" din "{sys.argv[2]}" este acceptat de masina!')
                if equalTapes:
                    print("Benzile sunt identice.")
                else:
                    print("Benzile nu sunt identice. Exista diferențe intre banda princapala si cea de backup.")
            elif flag == 4:
                print(f'Sirul "{string}" din "{sys.argv[2]}" nu este acceptat de masina.')


            print("----------------------------------", flag)

        inputTM.close()
except:
        print("Fișierul solicitat nu există sau altceva a mers prost.")


