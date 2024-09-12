import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(corps):
    expediteur = "koffimissy0000@gmail.com"
    mot_de_passe = "audp scfx czwe wrvl" 
    destinataire = "awgsabidjan.pay@gmail.com"
    sujet = "Commande BAOBOA"  

    serveur_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    serveur_smtp.starttls()
    
    try:
        # Se connecter au compte Gmail
        serveur_smtp.login(expediteur, mot_de_passe)
        
        # Créer le message
        message = MIMEMultipart()
        message['From'] = expediteur
        message['To'] = destinataire
        message['Subject'] = sujet
        
        # Ajouter le corps du message
        message.attach(MIMEText(f'Eastpak-shop - {corps}', 'plain'))
        
        # Envoyer l'email
        serveur_smtp.send_message(message)
        print("L'email a été envoyé avec succès!")
    
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return 'error'
    
    finally:
        serveur_smtp.quit()

    return 'success'
