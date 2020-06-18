## Up and Down the River

Up and Down the River is a simple trick taking card game for 3 to 8 players (AKA "Oh Hell")

## Overview

The object of the game is simple, each player is dealt a card(s) corresponding to the current round of the game (starts at 1!).  After each player has their designated cards for the given round, the remaining deck is placed in the middle and the top card is flip up to reveal the "trick suit".  This suit determines the "trick suit" for each round of play.  Bidding then commences.  The objective of the round (and game) is to bid the number of tricks you will take.  Each player plays one card until all cards have been discarded.  Score is then determined based on how many tricks you bid vs. how many you actual took during play.

## Installation

You will need to install Pygame in order to run this game.  If installed, run the game through terminal (src folder):

```bash
$ python game.py
```

## Gameplay

Each hand starts with the player to the left of the dealer.  Once the bidding round has been complete, the same player to the left of the dealer opens the play.  Their suit determines what must be played if any subsequent player has that suit in their hand of cards.  If a player does not have the opening suit played, they can play a "trick" by playing any card.  The winning hand of each round will be the highest value of card played (Ace is high, 2 is low).  However, any trick card (trick suit determined each deal) will trump any card, even the suit that was originally played.  As with other cards, trick cards with the highest value (Ace is high, 2 is low) will trump other trick cards of the same trick suit.  The Joker (and there is only one in the deck) is the Ultimate card.  The Joker automatically becomes the top valued trick card in the hand.  The winner of each hand will begin play for the next hand.  A round is complete when every card has been played from your hand.

## Specific Rules

At the beginning of each hand, the first player can play any card from their hand, except a trick suit UNLESS one of the two circumstances is true - 1) They only have cards of the trick suit in their hand, or 2) The trick suit has been "broken".  A trick suit can only be played if a player doesn't have the suit of the original play in their current hand.

## Scoring

Scoring is quite simple, for each round you will receive 10 points for correctly taking the number of tricks you bid, plus a bonus point for the number you bid (i.e. 10 points award for successful 0 bid, 13 points awarded for successful 3 bid).  0 points will be given if you miss your bid total.  Highest score at the end of the game wins!
