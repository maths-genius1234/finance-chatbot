def main():
    user_data = {
        'name': '',
        'balance': 0.0,
        'cart': []
    }

    print("🛍️ Welcome to BudgetBuddy - Your Personal Shopping Assistant! 💸\n")
    user_data['name'] = input("📝 Please enter your name to start: ")
    print(f"\n👋 Hi {user_data['name']}! How can I assist you today?\n")
    print("💡 Type '/help' to see available commands.\n\n")

    while True:
        command = input("➡️  ").strip()
        if not command:
            continue

        parts = command.split()
        cmd = parts[0].lower()

        if cmd == '/exit':
            if len(parts) > 1:
                print("\n❌ Invalid command. '/exit' doesn't accept arguments.")
                print("💡 Correct usage: /exit\n")
                continue
            confirm = input("\n❗ Are you sure you want to exit? (yes/no): ").lower()
            if confirm == 'yes':
                print(f"\n👋 Goodbye, {user_data['name']}! Happy shopping! 🛍️\n")
                break
            else:
                print("\n🚫 Exit canceled. Continuing with BudgetBuddy!\n")
                continue

        if cmd == '/help':
            if len(parts) > 1:
                print("\n❌ Invalid command. '/help' doesn't accept arguments.")
                print("💡 Correct usage: /help\n")
                continue
            print("\n📚 Available Commands:\n")
            print("/help - Show this help message")
            print("/cart view - View your shopping cart")
            print("/cart add {item} {cost} - Add an item to the cart")
            print("/cart remove {item} {cost} - Remove an item from the cart")
            print("/cart analyze - Analyze your shopping cart")
            print("/cart empty - Empty your shopping cart")
            print("/balance - View your current balance")
            print("/balance set {amount} - Set your available balance")
            print("/exit - Exit the program\n")

        elif cmd == '/cart':
            if len(parts) < 2:
                print("\n❌ Invalid cart command. Use '/help' for instructions.\n")
                continue

            subcmd = parts[1].lower()

            if subcmd == 'view':
                if len(parts) > 2:
                    print("\n❌ Invalid command. '/cart view' doesn't accept arguments.")
                    print("💡 Correct usage: /cart view\n")
                    continue
                if not user_data['cart']:
                    print("\n🛒 Your cart is empty. 🌫️\n")
                else:
                    print("\n🛒 Items in your cart:")
                    for idx, item in enumerate(user_data['cart'], 1):
                        print(f"🔸 {idx}. {item['name']} - ${item['cost']:.2f}")
                    total = sum(item['cost'] for item in user_data['cart'])
                    print(f"\n💵 Total cost: ${total:.2f}")
                    print(f"📉 Remaining balance: ${user_data['balance']:.2f}\n")

            elif subcmd == 'add':
                if len(parts) != 4:
                    print("\n❌ Invalid format. '/cart add' requires exactly 2 arguments.")
                    print("💡 Correct usage: /cart add {item} {cost}\n")
                    continue

                try:
                    cost = float(parts[-1])
                    item_name = ' '.join(parts[2:-1])
                    if cost <= 0:
                        print("\n❌ Cost must be a positive number. 🔢\n")
                        continue

                    if user_data['balance'] <= 0 and user_data['balance'] != float('inf'):
                        print("\n💳 Please set your balance using '/balance set' before adding items. ⚠️\n")
                        continue

                    if cost >= 100:
                        confirm = input(f"\n⚠️ 💸 This item costs ${cost:.2f}. Are you sure? (yes/no): ").lower()
                        if confirm != 'yes':
                            print("\n🚫 Item not added.\n")
                            continue

                    if cost > user_data['balance']:
                        confirm = input(f"\n⚠️ 📉 This will exceed your balance by ${cost - user_data['balance']:.2f}. Continue? (yes/no): ").lower()
                        if confirm != 'yes':
                            print("\n🚫 Item not added.\n")
                            continue

                    user_data['cart'].append({'name': item_name, 'cost': cost})
                    user_data['balance'] -= cost
                    print(f"\n✅ Added '{item_name}' (${cost:.2f}) to cart! 🛒 Remaining balance: ${user_data['balance']:.2f} 💰\n")

                except ValueError:
                    print("\n❌ Invalid cost. Please enter a valid number. 🔢\n")

            elif subcmd == 'remove':
                if len(parts) != 4:
                    print("\n❌ Invalid format. '/cart remove' requires exactly 2 arguments.")
                    print("💡 Correct usage: /cart remove {item} {cost}\n")
                    continue

                try:
                    cost = float(parts[-1])
                    item_name = ' '.join(parts[2:-1])
                    found = False

                    for item in user_data['cart']:
                        if item['name'] == item_name and item['cost'] == cost:
                            user_data['cart'].remove(item)
                            user_data['balance'] += cost
                            found = True
                            print(f"\n✅ Removed '{item_name}' (${cost:.2f})! 🗑️ New balance: ${user_data['balance']:.2f} 💰\n")
                            break

                    if not found:
                        print(f"\n🔍 Item '{item_name}' with cost ${cost:.2f} not found in cart. ❌\n")

                except ValueError:
                    print("\n❌ Invalid cost format. Please use numbers. 🔢\n")

            elif subcmd == 'analyze':
                if len(parts) > 2:
                    print("\n❌ Invalid command. '/cart analyze' doesn't accept arguments.")
                    print("💡 Correct usage: /cart analyze\n")
                    continue
                total_cost = sum(item['cost'] for item in user_data['cart'])
                print("\n📊 🛒 Cart Analysis:")
                print(f"🔢 Total items: {len(user_data['cart'])}")
                print(f"💸 Total cost: ${total_cost:.2f}")
                print(f"📉 Remaining balance: ${user_data['balance']:.2f}")

                if user_data['balance'] < 0:
                    print("\n⚠️ ❗ Warning: Your balance is negative! 💸\n")
                elif user_data['balance'] < 50:
                    print("\nℹ️ 💰 Your remaining balance is getting low. ⚠️\n")

                if user_data['cart']:
                    avg = total_cost / len(user_data['cart'])
                    print(f"\n📈 Average item cost: ${avg:.2f}")
                    most_expensive = max(user_data['cart'], key=lambda x: x['cost'])
                    print(f"🏆 Most expensive item: {most_expensive['name']} (${most_expensive['cost']:.2f}) 💸\n")

            elif subcmd == 'empty':
                if len(parts) > 2:
                    print("\n❌ Invalid command. '/cart empty' doesn't accept arguments.")
                    print("💡 Correct usage: /cart empty\n")
                    continue
                confirm = input("\n❗ Are you sure you want to empty your cart? (yes/no): ").lower()
                if confirm == 'yes':
                    total_removed = sum(item['cost'] for item in user_data['cart'])
                    user_data['balance'] += total_removed
                    user_data['cart'].clear()
                    print("\n✅ Cart emptied! 🗑️ Balance updated. 💰\n")
                else:
                    print("\n🚫 Cart emptying canceled.\n")

            else:
                print("\n❌ Invalid cart command. Use '/help' for instructions. ⚠️\n")

        elif cmd == '/balance':
            if len(parts) == 1:
                print(f"\n💰 Current balance: ${user_data['balance']:.2f} 💵\n")
            elif parts[1].lower() == 'set':
                if len(parts) != 3:
                    print("\n❌ Invalid format. '/balance set' requires exactly 1 argument.\n")
                    print("💡 Correct usage: /balance set {amount}\n")
                    continue
                try:
                    new_balance = float(parts[2])
                    if new_balance < 0:
                        print("\n❌ Balance cannot be negative. ⚠️\n")
                    else:
                        user_data['balance'] = new_balance
                        print(f"\n✅ Balance set to ${new_balance:.2f} 💰\n")
                except ValueError:
                    print("\n❌ Invalid amount. Please enter a number. 🔢\n")
            else:
                print("\n❌ Invalid balance command. Use '/help' for instructions. ⚠️\n")

        else:
            print("\n❌ Invalid command. Type '/help' for available commands. ⚠️\n")

if __name__ == "__main__":
    main()
