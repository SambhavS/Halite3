# Halite 3 Bot (Greedy Heurestic Approach)
Here's the Python code for my Halite 3 bot. Halite 3 was a programming competition hosted by Two Sigma where bots control turtles that fight to collect the maximum amount of halite, the game currency.


I ranked #655 out of ~4000 entrants, putting me narrowly in the top sixth. (https://halite.io/user/?user_id=8525)
I also think I got the highest score of the (not that many) Berkeley undergrads who competed this year.

## Strategic Summary
My whole program was about 150 lines and followed a fairly simple greedy heurestic-based strategy.

Here are some ideas that influenced my design:

1) We can approximate the value of each square and set the square with the highest expected value as our target. I used distance and halite as my heuristics for this. After playing around with a couple variations of this, I stuck with calculating the amount of halite/turn and discounted squares that were further away. Weak exponential discounting seemed to work best, but I have little idea why. Every turn, I would update targets. To help me with this, I tried finding a threshold of when to stop mining halite and stuck with 50 which seemed to work well.

2) Once a target was chosen, I had my turtles greedily navigate towards it; if a target was upwards and leftwards, a turtle would go left or up based on how much halite was there.

3) Turtles are (typically) most valuable if they are born early and have the rest of the game to collect halite. I spawned 20 turtles as fast as I could and then stopped. I played around with spawning based on how much halite I had and how many turns were left, but neither did measurably better.

4) After turtles were mostly full, I had them greedily return to the spawn point. I let them keep a little bit of space so they could absorb halite if they happened to come across any particularly good deposits on their way back.

5) To avoid clogging, I had turtles move away from the target after depositing halite and also had them move randomly if they were not in a spot much halite around. Adding some randomness was also helpful for preventing clustering or missed deposits.

6) Once the game was coming to the end, I crashed all my turtles into the center to eke out whatever remaining halite they were carrying. I triggered this when I had thirty turns left to go.

It was really interesting to write a program based on lots of testing and greedy heuristics as opposed to strictly logical/algorithmic rules (like I'm used to). I was surprised that tuning and tweaking a lot of variables by hand led to pretty big improvements. 

Having looked at a few of the post-mortem write-ups of the people who did a lot better than me, I think I could have improved a little by having better heurestics and improving a lot by having better pathing that allowed for turtle swapping. This was my first time doing Halite and I thought it was overall a lot of fun and definitely recommend it!


