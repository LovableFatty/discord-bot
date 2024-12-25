# **AI-Noah-Bucks Discord Bot**

A Discord bot for managing quests and a virtual currency system, **AI-Noah-Bucks**. The bot allows an authorized user to create and manage quests, award or deduct currency, and track player balances.

---

## **Features**

- **Quest Management:** Create, list, and complete quests. Reward players upon quest completion.
- **Currency System:** Award, deduct, and check AI-Noah-Bucks balances.
- **Modular Codebase:** Organized into logical modules for easy scalability.

---

## **Setup**

### **Prerequisites**

- Python 3.10+
- Required libraries: `discord.py`, `python-dotenv`

### **Installation**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd discord-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up .env
4. Run the bot
   ```bash
   python bot.py
   ```

## **Commands**

### **Quest Management**

- `!create_quest <reward> <description>`: Create a new quest.
- `!list_quests`: List available quests.
- `!complete_quest <quest_id> @player`: Complete a quest and reward a player.
- `!completed_quests`: List completed quests.

### **Currency Management**

- `!balance [@player]`: Check AI-Noah-Bucks balance.
- `!award @player <amount>`: Award currency to a player.
- `!deduct @player <amount>`: Deduct currency from a player.

## **File Structure**

```bash
discord_bot/
├── bot.py            # Main bot script
├── commands/         # Contains commands modules
│   ├── balances.py   # Commands for managing balances
│   ├── quests.py     # Commands for managing quests
├── database.py       # Database setup and helpers
├── utils.py          # Utility functions
├── .env              # Environment variables
└── requirements.txt  # Dependencies

```
