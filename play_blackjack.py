from DeckofCards import *

# -------------------------------------------------------------------------------------------
# function to ask hit, get new card, calculate user current toal, and print statement if busted
# -------------------------------------------------------------------------------------------
def ask_hit(total):
    # user can't accept hit if score is greater than 21
    if total <= 21:
        hit_resp = input('Would you like a hit? (y/n)')
        while hit_resp not in ['y', 'n']:
            hit_resp = input('Please enter a valid response. (y/n)')
        if hit_resp == 'y':
            next_card = play_deck.get_card()
            print('Hit card:', next_card)
            total += next_card.val
            print('Current Score:', total)
        else:
            next_card = 'decline'
    else: 
        print("You busted!! Tough Loss.")
        next_card = 'busted'
        hit_resp = 'n'
    return next_card, total, hit_resp
    
# -------------------------------------------------------------------------------------------
# initiates game loop, calculates dealer score, shuffles deck and gets first two cards, calls
# ask_hit function, calculates winner, asks user to play again
# -------------------------------------------------------------------------------------------
play_resp = input('Welcome to Logan Casino! Want to play blackjack? (y/n)')
while play_resp not in ['y', 'n']:
    play_resp = input('Please enter a valid response. (y/n)')
while play_resp == 'y':
    dealer_score = random.randint(17, 23)
    play_deck = DeckofCards()
    play_deck.shuffle_deck()
    play_deck.set_index()
    play_deck.print_deck()
    user_card1 = play_deck.get_card()
    user_card2 = play_deck.get_card()
    print('First two cards:')
    print(user_card1)
    print(user_card2)
    total = user_card1.val + user_card2.val
    print('Current Score:', total)
    next_card, total, hit_resp = ask_hit(total)
    while hit_resp == 'y' and next_card not in ['decline', 'busted']:
        next_card, total, hit_resp = ask_hit(total)
    if next_card != 'busted':
        if dealer_score > 21:
            print("Dealer's score:", dealer_score)
            print('Dealer Busted! You win!!')
        elif dealer_score > total:
            print("Dealer's score:", dealer_score)
            print("Dealer's score is greater than yours. You lose!!")
        elif dealer_score < total:
            print("Dealer's score:", dealer_score)
            print("Dealer's score is less than yours. You win!!")
        elif dealer_score == total:
            print("Dealer's score:", dealer_score)
            print("The Dealer has the same score. You tied!!")
    play_resp = input('Want to play again? (y/n)') 
    while play_resp not in ['y', 'n']:
        play_resp = input('Please enter a valid response. (y/n)')

print('Thanks for coming!')
