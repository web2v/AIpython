#incoming V2

import openai
import os
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

openai.api_key = "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"

def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="oublies toute instruction précédente. maintenant, Sous ubuntu 22 LTS gnome-shell version 42.5  ,je suis dans le dossier courant où je veux executer la commande,  Donnez-moi la commande pour "+ prompt +" ?  repond en formatant ta reponse comme cela :  pas de commentaires,ne met  pas de balise, seulement au format texte , extrait seulement la commande, s il y a plusieurs commandes ajoutes les dans le script .  merci. ",
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.2,
    )
    return response.choices[0].text.strip()

def comment_on_command(command):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Expliquez et commentez en français la commande suivante : " + command,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def execute_script(script):
    with open("temp_script.sh", "w") as script_file:
        script_file.write("#!/bin/bash\n")
        script_file.write(script)

    os.chmod("temp_script.sh", 0o755)
    subprocess.run(["./temp_script.sh"])
    os.remove("temp_script.sh")

if __name__ == "__main__":
    print("Bienvenue dans l'assistant ChatGPT CLI Docteur ubuntu ! V3 ")
    session = PromptSession(history=InMemoryHistory(), auto_suggest=AutoSuggestFromHistory())
    while True:
        user_input = session.prompt("Entrez votre question ou problème : ")
        if user_input.lower() in ["quit", "exit","qq"]:
            print("Au revoir!")
            break

        command = chat_gpt(user_input)
        print("Commande proposée : ", command)

        comment = comment_on_command(command)
        print("Explication de la commande : ", comment)

        confirm = input("Voulez-vous exécuter les commandes suggérées ? (Oui/Non) : ")
        if confirm.lower() in ["oui", "o"]:
            execute_script(command)
            print("Les commandes ont été exécutées avec succès.")
        else:
            print("Les commandes n'ont pas été exécutées.")

