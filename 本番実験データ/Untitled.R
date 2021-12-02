install.packages("tidyverse")
library(tidyverse)

user_info_ls00 <- distinct(res_user_info_ls00)
predictions_ls00 <- distinct(res_predictions_ls00)
estimations_ls00 <- distinct(res_estimations_ls00)



write.csv(estimation_ls00, "estimations_ls00.csv")
