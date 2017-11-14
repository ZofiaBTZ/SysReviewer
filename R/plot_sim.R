#setwd("../../../Genf/sysRevieweGH/")
symSim <- read.csv("SymSim.csv", stringsAsFactors=FALSE)
sim <- read.csv("AsymSim.csv", stringsAsFactors=FALSE)
symSim <- na.omit(symSim)
sim <- na.omit(sim)
rownames(sim) <-  sim[,2]
sim <- sim[,-c(1,2)]
colnames(sim) <-rownames(sim)[-1]
sim <- sim[-1,]


rownames(symSim) <-  symSim[,2]
symSim <- symSim[,-c(1,2)]
colnames(symSim) <-rownames(symSim)[-1]
symSim <- symSim[-1,]

sim_num <- matrix(0, nrow = nrow(sim), ncol = nrow(sim))
rownames(sim_num) <- rownames(sim)
colnames(sim_num) <- colnames(sim)

for (i in c(1:nrow(sim))){
  for (j in c(1:nrow(sim))){
     sim_num[i,j] <- (as.numeric(symSim[i,j])) 
      #round(as.numeric(sim[i,j]), digits = 3) 
 #    sim[i,j] <- as.numeric(sim[i,j])
}}
View(sim_num)
a <- heatmap(sim_num)
tree <- heatplot(log(sim_num+1), returnSampleTree = TRUE)

#hc <- hclust(log(sim_num + 1))
#hc_cut <- cutree(hc,10)