# Artifact_Analyser
A py program to analyse artifacts in genshin impact

Analysis includes: 
1. calculation and Filtering of artifacts w.r.t total roll value
2. provide comparison between current good artifacts vs potentially good unlevelled artifacts
3. For unleveled artifacts get 99.9% accurate statistical representaion of expected roll value and chance to get above a certain total roll value



Developed a Python-based tool that analyzes artifacts from a game "Genshin Impact" using data exported from the Inventory Kamera app.
context: This game has a player stat system, that can be boosted by items called artifacts. 
        These artifacts can be upgraded, but their stats are determined by a random sytem.
        A player typically receives ~1000 artificats from which they have to  choose which artifact to upgrade.
This program reduces the load on players by automating their selection by taking data form the game using a on screen parser called Kamera app (allowed by the game), returns a json format of the data scanned.
The data is extracted and analyzed to build a statistical distribution of the top performing artifacts.
(note: 2 distributions: 1 with respect to weighted chance of being good, 2nd the top performing artifacts with a threshold chance).
The output is translated to a excel format, by converting the rows of data into 2D arrays. And written into an excel file.

---details regarding method on statistics, skip to end of this description---
Each artifact can be upgraded 5 times, and there are 4 stats for each artifact (which are called "sub stats").
Each of time a artifact is upgraded a random "sub stat" among the said 4 is also upgraded.
The number of times and quality of these substats are what determines a good artifact. To solve the statistical distribution of this complex problem binomial theorem formula was used.
Each sub stat is weighted, as the resultant of all the stats in the game is damage.
The binomial thorem here provides chances for reaching a certain level of the total weighted substat.
Now there are multiple substats, By adding all subtats for a gives upgrade sequence, we get the performance of a artifact.
So with the performance to chance data for each artifact, 2 distributions are made:
        1) with respect to average roll (Chance x performance)
        2) with respect to top performing artifacts (provided it crosses a threshold chance, i.e. if the chance is above say 5% it will be ranked by the performance else it is ignored

This distribution is then logged to a excel, ranking appearing a column of values, with the artifact name, its sub stats and calculated chances.


