import os
import logging
import asyncpg
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database connection
db_pool = None

# Conversation states
NAME, AGE, GENDER, UNIVERSITY, BIO = range(5)

# **ALL ETHIOPIAN UNIVERSITIES (45+ INSTITUTIONS)**
ETHIOPIAN_UNIVERSITIES = [
    # Government Universities
    "Addis Ababa University",
    "Addis Ababa Science and Technology University",
    "Adama Science and Technology University",
    "Adigrat University",
    "Aksum University",
    "Ambo University",
    "Arba Minch University",
    "Assosa University",
    "Bahir Dar University",
    "Bule Hora University",
    "Debre Berhan University",
    "Debre Markos University",
    "Debre Tabor University",
    "Dilla University",
    "Dire Dawa University",
    "Gambella University",
    "Gondar University",
    "Haramaya University",
    "Hawassa University",
    "Injibara University",
    "Jimma University",
    "Jigjiga University",
    "Kebri Dehar University",
    "Madda Walabu University",
    "Mekelle University",
    "Mizan-Tepi University",
    "Semera University",
    "Wachemo University",
    "Wolaita Sodo University",
    "Wollega University",
    "Wollo University",
    
    # Private Universities
    "St. Mary's University",
    "Unity University",
    "Rift Valley University",
    "Kea-Med University",
    "New Generation University",
    "HiLCoE School of Computer Science",
    "Ethiopian Civil Service University",
    "Defense University",
    "Kotebe Metropolitan University",
    "Abera University",
    "Alkan University",
    "Bethel University",
    "Jiren University",
    "Omega University",
    "Admas University"
]

# **Database Setup**
async def init_db():
    global db_pool
    db_pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))
    await create_tables()

async def create_tables():
    async with db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                username TEXT,
                name TEXT NOT NULL,
                age INTEGER CHECK (age >= 18 AND age <= 35),
                gender TEXT CHECK (gender IN ('Male', 'Female')),
                university TEXT NOT NULL,
                bio TEXT,
                profile_complete BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                user1_id BIGINT REFERENCES users(id),
                user2_id BIGINT REFERENCES users(id),
                created_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (user1_id, user2_id)
            )
        ''')

# **Bot Handlers**
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with db_pool.acquire() as conn:
        exists = await conn.fetchval('SELECT 1 FROM users WHERE id = $1', user.id)
        if exists:
            await update.message.reply_text("Welcome back! Use /browse to find matches.")
            return ConversationHandler.END
    
    await update.message.reply_text(
        "👋 Welcome to **Ethiopian Uni Dating Bot**!\n"
        "Let's create your profile.\n\n"
        "What's your **name**? (First name only)"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name or len(name) > 50:
        await update.message.reply_text("Please enter a valid name (1-50 characters).")
        return NAME
    
    async with db_pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO users (id, name) VALUES ($1, $2) '
            'ON CONFLICT (id) DO UPDATE SET name = $2',
            update.effective_user.id, name
        )
    
    await update.message.reply_text(f"Nice, {name}! How **old** are you? (18-35)")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        if not 18 <= age <= 35:
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid age (18-35):")
        return AGE
    
    async with db_pool.acquire() as conn:
        await conn.execute(
            'UPDATE users SET age = $1 WHERE id = $2',
            age, update.effective_user.id
        )
    
    keyboard = [["Male", "Female"]]
    await update.message.reply_text(
        "What's your **gender**?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gender = update.message.text
    if gender not in ["Male", "Female"]:
        await update.message.reply_text("Please select **Male** or **Female**:")
        return GENDER
    
    async with db_pool.acquire() as conn:
        await conn.execute(
            'UPDATE users SET gender = $1 WHERE id = $2',
            gender, update.effective_user.id
        )
    
    keyboard = [[uni] for uni in ETHIOPIAN_UNIVERSITIES]
    await update.message.reply_text(
        "🏫 Select your **university**:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return UNIVERSITY

async def get_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uni = update.message.text
    if uni not in ETHIOPIAN_UNIVERSITIES:
        await update.message.reply_text("Please select from the list:")
        return UNIVERSITY
    
    async with db_pool.acquire() as conn:
        await conn.execute(
            'UPDATE users SET university = $1 WHERE id = $2',
            uni, update.effective_user.id
        )
    
    await update.message.reply_text(
        "📝 Write a short **bio** (max 200 chars):\n"
        "(Interests, hobbies, what you're looking for)",
        reply_markup=ReplyKeyboardRemove()
    )
    return BIO

async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bio = update.message.text[:200]
    async with db_pool.acquire() as conn:
        await conn.execute(
            'UPDATE users SET bio = $1, profile_complete = TRUE WHERE id = $2',
            bio, update.effective_user.id
        )
    
    await update.message.reply_text(
        "🎉 **Profile complete!** Use /browse to find matches."
    )
    return ConversationHandler.END

async def browse_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    async with db_pool.acquire() as conn:
        # Check if profile is complete
        if not await conn.fetchval('SELECT profile_complete FROM users WHERE id = $1', user.id):
            await update.message.reply_text("❌ Complete your profile first with /start")
            return
        
        # Get user's gender and university
        user_data = await conn.fetchrow(
            'SELECT gender, university FROM users WHERE id = $1', user.id
        )
        target_gender = "Female" if user_data['gender'] == "Male" else "Male"
        
        # Find compatible matches
        match = await conn.fetchrow('''
            SELECT u.id, u.name, u.age, u.university, u.bio
            FROM users u
            WHERE u.gender = $1
            AND u.university = $2
            AND u.id != $3
            AND u.profile_complete = TRUE
            AND NOT EXISTS (
                SELECT 1 FROM matches
                WHERE (user1_id = $3 AND user2_id = u.id)
                OR (user1_id = u.id AND user2_id = $3)
            )
            ORDER BY RANDOM()
            LIMIT 1
        ''', target_gender, user_data['university'], user.id)
        
        if not match:
            await update.message.reply_text("No more profiles in your university. Try later!")
            return
        
        context.user_data['current_match'] = match['id']
        
        # Display profile
        profile_msg = (
            f"👤 **{match['name']}**, {match['age']}\n"
            f"⚧️ **{target_gender}**\n"
            f"🏫 **{match['university']}**\n\n"
            f"📝 *{match['bio']}*"
        )
        
        keyboard = [
            [InlineKeyboardButton("❤️ Like", callback_data="like"),
             InlineKeyboardButton("➡️ Skip", callback_data="skip")]
        ]
        await update.message.reply_text(
            profile_msg,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    target_id = context.user_data['current_match']
    action = query.data
    
    async with db_pool.acquire() as conn:
        # Record interaction
        await conn.execute(
            'INSERT INTO matches (user1_id, user2_id) VALUES ($1, $2)',
            min(user_id, target_id), max(user_id, target_id)
        )
        
        # Notify if match
        if action == 'like':
            mutual_like = await conn.fetchval('''
                SELECT 1 FROM matches
                WHERE user1_id = $1 AND user2_id = $2
            ''', target_id, user_id)
            
            if mutual_like:
                user_name = await conn.fetchval('SELECT name FROM users WHERE id = $1', user_id)
                target_name = await conn.fetchval('SELECT name FROM users WHERE id = $1', target_id)
                
                await context.bot.send_message(
                    user_id,
                    f"💑 **You matched with {target_name}!**\n"
                    f"Send them a message! 💬"
                )
                await context.bot.send_message(
                    target_id,
                    f"💑 **You matched with {user_name}!**\n"
                    f"Send them a message! 💬"
                )
    
    await query.edit_message_text(
        text=f"You {'❤️ liked' if action == 'like' else '➡️ skipped'} this profile."
    )
    await browse_profiles(update, context)

def setup_application():
    application = ApplicationBuilder() \
        .token(os.getenv('BOT_TOKEN')) \
        .post_init(post_init) \
        .build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT, get_name)],
            AGE: [MessageHandler(filters.TEXT, get_age)],
            GENDER: [MessageHandler(filters.TEXT, get_gender)],
            UNIVERSITY: [MessageHandler(filters.TEXT, get_university)],
            BIO: [MessageHandler(filters.TEXT, get_bio)]
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: ConversationHandler.END)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('browse', browse_profiles))
    application.add_handler(CallbackQueryHandler(handle_interaction))
    
    return application

async def post_init(application):
    await init_db()

application = setup_application()
async def initialize_bot():
    """Initialize the bot application"""
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
