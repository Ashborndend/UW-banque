import sqlite3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from datetime import datetime
from telegram.helpers import escape_markdown

# Connexion à la base SQLite
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table utilisateurs si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    prestige INTEGER DEFAULT 0,
    flocons INTEGER DEFAULT 0,
    apparition TEXT
)
""")
conn.commit()

# Ajouter l'utilisateur spécial @ROI0END si absent
def init_roi():
    cursor.execute("SELECT * FROM utilisateurs WHERE user_id = ?", (5330541181,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO utilisateurs (user_id, username, prestige, flocons, apparition)
            VALUES (?, ?, ?, ?, ?)
        """, (5330541181, "ROI0END", 999999, 99999, "01/01/2025"))
        conn.commit()
init_roi()

def obtenir_grade(prestige):
    if prestige < 10: return "Recrue", 10
    elif prestige < 50: return "Soldat", 50
    elif prestige < 150: return "Soldat de 1ère classe", 150
    elif prestige < 500: return "Sergent", 500
    elif prestige < 1000: return "Lieutenant", 1000
    elif prestige < 2000: return "Major", 2000
    elif prestige < 5000: return "Amiral", 5000
    elif prestige < 10000: return "Centurion", 10000
    elif prestige < 20000: return "Souverain", 20000
    else: return "Empereur", 100000

def obtenir_rang(flocons):
    if flocons < 100: return "Dormeur", 100
    elif flocons < 500: return "Éveillé", 500
    elif flocons < 1000: return "Ascendant", 1000
    elif flocons < 2000: return "Transcendant", 2000
    elif flocons < 10000: return "Sacré", 10000
    else: return "Divin", 20000

def get_user(user):
    cursor.execute("SELECT * FROM utilisateurs WHERE user_id = ?", (user.id,))
    result = cursor.fetchone()
    if not result:
        apparition = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("INSERT INTO utilisateurs (user_id, username, apparition) VALUES (?, ?, ?)",
                       (user.id, user.username or user.first_name, apparition))
        conn.commit()
        return (user.id, user.username or user.first_name, 0, 0, apparition)
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        bouton1 = [
        [InlineKeyboardButton("ICI", url="https://t.me/Soldierendbot")]
    ]
        await update.message.reply_text("⛔ Cette commande ne peut être utilisée que dans le bot", reply_markup=InlineKeyboardMarkup(bouton1))
        return
    get_user(update.effective_user)
    message = """*Bienvenue*, tu viens de franchir la première porte de l’Empire *Urban Wolf*.

📜 *Commandes disponibles :*
\n/start – Démarre le bot
\n/statut – Ton rang
\n/flocon – Infos sur la monnaie ❄️
\n/prestige – Infos sur les points ✨
\n/classement – Voir les meilleurs
\n/link – Lien de l'empire
\n/give – Donner des flocons ❄️
"""
    await update.message.reply_photo(photo="https://imgur.com/a/xug47FR", caption=message, parse_mode="Markdown")

async def statut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = get_user(update.effective_user)
    grade, prochain_prestige = obtenir_grade(user_data[2])
    rang, prochain_flocon = obtenir_rang(user_data[3])
    message = f"""[𓆩 @{user_data[1]} 𓆪]

🎖️ Grade : {grade}
✨ Prestige : {user_data[2]} ✨ / {prochain_prestige}
️️🏅 Rang : {rang}
❄️ Flocons : {user_data[3]} ❄️ / {prochain_flocon}
️📆 Apparu le : {user_data[4]}"""
    await update.message.reply_photo(photo="https://imgur.com/a/m2USWEy", caption=message, parse_mode="Markdown")

async def prestige(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✨ Prestige — Honneur et Loyauté Attribué par l’Empereur ou ses Généraux. C’est la marque de ton dévouement absolu à l’Empire.\n\n🎖️ Grades (Prestige) :\n\n✪ Recrue : 0 – 10\n\n✪ Soldat : 10 – 50\n\n✪ 1ère Classe : 50 – 150\n\n✪ Sergent : 150 – 500\n\n✪ Lieutenant : 500 – 1 000\n\n✪ Major : 1 000 – 2 000\n\n✪ Amiral : 2 000 – 5 000\n\n✪ Centurion : 5 000 – 10 000\n\n✪ Souverain : 10 000 – 20 000\n\n✪ Empereur : 100 000+ (réservé)\n\n🔥 Comment gagner du ✨ Prestige ?\n• Accomplir une mission secrète\n• Remporter un événement majeur\n• Être repéré par un supérieur\n• Accomplir un acte remarquable", parse_mode="Markdown")

async def flocon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❄️ Flocons — Monnaie du Pouvoir Utilise-les pour débloquer des privilèges, gravir les échelons ou obtenir des récompenses exclusive.\n\n🏆 Rangs (Flocons) :\n\n✪ Dormeur : 0 – 100\n\n✪ Éveillé : 100 – 500\n\n✪ Ascendant : 500 – 1 000\n\n✪ Transcendant : 1 000 – 2 000\n\n✪ Sacré : 2 000 – 10 000\n\n✪ Divin : 10 000+\n\n⚙️ Comment gagner des ❄️ Flocons ?\n• Gagner un duel contre un admin (événement validé)\n• Créer ou organiser un événement\n• Remporter un événement officiel\n• Réaliser un exploit ou aider activement l’Empire", parse_mode="Markdown")

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
        bouton1 = [
        [InlineKeyboardButton("Rejoins l'Empire", url="https://t.me/MILITARY_URBANWOLF")]
    ]
        await update.message.reply_text("Voici le lien", reply_markup=InlineKeyboardMarkup(bouton1))

async def classement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boutons = [[InlineKeyboardButton("Flocons ❄️", callback_data="classement_flocon")],
               [InlineKeyboardButton("Prestige ✨", callback_data="classement_prestige")]]
    await update.message.reply_text("Choisis :", reply_markup=InlineKeyboardMarkup(boutons))

async def bouton_classement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "classement_flocon":
        cursor.execute("SELECT username, flocons FROM utilisateurs ORDER BY flocons DESC")
        tri = cursor.fetchall()
        titre = "🏆 *Classement Flocons ❄️*\n\n"
        lignes = []
        for i, user in enumerate(tri):
            pseudo = escape_markdown(user[0] or "Inconnu", version=2)
            lignes.append(f"{i+1}\. @{pseudo} – {user[1]} ❄️")
    else:
        cursor.execute("SELECT username, prestige FROM utilisateurs ORDER BY prestige DESC")
        tri = cursor.fetchall()
        titre = "🏅 *Classement Prestige ✨*\n\n"
        lignes = []
        for i, user in enumerate(tri):
            pseudo = escape_markdown(user[0] or "Inconnu", version=2)
            lignes.append(f"{i+1}\. @{pseudo} – {user[1]} ✨")

    texte_final = escape_markdown(titre, version=2) + "\n".join(lignes)
    await query.edit_message_text(text=texte_final, parse_mode="MarkdownV2")
    
async def holy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != "ROI0END":
        await update.message.reply_text("⛔ Seul l'Empereur peut utiliser cette commande.")
        return
    if len(context.args) < 2 and not update.message.reply_to_message:
        await update.message.reply_text("Utilisation : /holy [flocons|prestige] [valeur] en répondant à un message.")
        return
    type_point = context.args[0].lower()
    valeur = int(context.args[1])
    cible = update.message.reply_to_message.from_user
    get_user(cible)
    cursor.execute(f"UPDATE utilisateurs SET {type_point} = {type_point} + ? WHERE user_id = ?", (valeur, cible.id))
    conn.commit()
    await update.message.reply_text(f"✅ Ajout de {valeur} {'❄️' if type_point == 'flocons' else '✨'} à @{cible.username}")

async def unholy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != "ROI0END":
        await update.message.reply_text("⛔ Seul l'Empereur peut utiliser cette commande.")
        return
    if len(context.args) < 2 and not update.message.reply_to_message:
        await update.message.reply_text("Utilisation : /unholy [flocons|prestige] [valeur] en répondant à un message.")
        return
    type_point = context.args[0].lower()
    valeur = int(context.args[1])
    cible = update.message.reply_to_message.from_user
    get_user(cible)
    cursor.execute(f"UPDATE utilisateurs SET {type_point} = MAX({type_point} - ?, 0) WHERE user_id = ?", (valeur, cible.id))
    conn.commit()
    await update.message.reply_text(f"☠️ Retrait de {valeur} {'❄️' if type_point == 'flocons' else '✨'} à @{cible.username}")

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or not update.message.reply_to_message:
        await update.message.reply_text("Utilisation : /give flocons [valeur] en répondant à un utilisateur.")
        return
    valeur = int(context.args[1])
    donneur = update.effective_user
    receveur = update.message.reply_to_message.from_user
    get_user(donneur)
    get_user(receveur)
    cursor.execute("SELECT flocons FROM utilisateurs WHERE user_id = ?", (donneur.id,))
    dispo = cursor.fetchone()[0]
    if dispo < valeur:
        await update.message.reply_text("❌ Tu n'as pas assez de flocons.")
        return
    cursor.execute("UPDATE utilisateurs SET flocons = flocons - ? WHERE user_id = ?", (valeur, donneur.id))
    cursor.execute("UPDATE utilisateurs SET flocons = flocons + ? WHERE user_id = ?", (valeur, receveur.id))
    conn.commit()
    await update.message.reply_text(f"✅ {valeur} ❄️ envoyé à @{receveur.username}")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 5330541181:
        await update.message.reply_text("⛔ Seul l'Empereur peut réinitialiser un utilisateur.")
        return

    cible = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if not cible:
        await update.message.reply_text("Réponds au message de l'utilisateur.")
        return

    cursor.execute("UPDATE utilisateurs SET prestige = 0, flocons = 0 WHERE user_id = ?", (cible.id,))
    conn.commit()
    await update.message.reply_text(f"🔄 Données de @{cible.username} réinitialisées.")


if __name__ == "__main__":
    app = ApplicationBuilder().token("7108384227:AAEBSsb36oH2Cdkg9-J0S7oJbGrhdsNweY8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("statut", statut))
    app.add_handler(CommandHandler("prestige", prestige))
    app.add_handler(CommandHandler("flocon", flocon))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CommandHandler("classement", classement))
    app.add_handler(CommandHandler("holy", holy))
    app.add_handler(CommandHandler("unholy", unholy))
    app.add_handler(CommandHandler("give", give))
    app.add_handler(CallbackQueryHandler(bouton_classement))
    app.add_handler(CommandHandler("kill", reset))

    print("Bot en ligne...")
    app.run_polling()
