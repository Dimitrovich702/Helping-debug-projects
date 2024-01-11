dataset <- read.csv("wdataset.csv")
head(dataset)
dim(dataset)
summary(dataset)
column <- dataset$ColumnName
filtered_data <- subset(dataset, column > threshold)
library(dplyr)
summary_by_group <- dataset %>%
  group_by(ColumnToGroup) %>%
  summarise(mean_value = mean(NumericColumn))

library(ggpubr)
ttest_results <- t.test(NumericColumn ~ CategoricalColumn, data = dataset)
plot(dataset$X, dataset$Y, xlab = "X", ylab = "Y", main = "Scatter plot")
hist(dataset$NumericColumn, main = "Histogram", xlab = "Values", ylab = "Frequency")
