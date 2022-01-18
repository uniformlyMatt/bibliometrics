using<-function(...) {
  libs<-unlist(list(...))
  req<-unlist(lapply(libs,require,character.only=TRUE))
  need<-libs[req==FALSE]
  if(length(need)>0){ 
    install.packages(need)
    lapply(need,require,character.only=TRUE)
  }
}

using("readxl","ggplot2","corrplot","PLNmodels","factoextra")

today <- format(Sys.time(), "%b_%d_%Y")

profiles <- read_excel("../Datasets/PCA_inputs_jan18.xlsx")

counts <- profiles[c(
  'citation_count',
  #'cited_by_count',
  'coauthor_count',
  'document_count',
  'h_index',
  'first_author_sum',
  'last_author_sum',
  'publication_duration',
  'openaccess_sum',
  'Article_sum'
)]
covariates <- profiles[c(
  'mean_citations_per_year',
  'growth_rate',
  'SJR_mean',
  'journal_h_index_mean',
  'author_count_mean',
  'mean_citations_per_doc',
  'chw_author_position_mean',
  'author_weight_mean',
  'Auid',
  'affil'
)]

df <- prepare_data(counts=counts, covariates=covariates)

PCAmodels <- PLNPCA(
  Abundance ~ 1 + #offset(log(Offset)) + 
    growth_rate + mean_citations_per_year +
    SJR_mean + journal_h_index_mean,# + author_weight_mean, #+
    #median_citations_per_doc + chw_author_position_median + author_count_median,
  data=df,
  ranks=1:9
)

bestICL <- getBestModel(PCAmodels, "ICL")
bestBIC <- getBestModel(PCAmodels, "BIC")
plot(bestICL, ind_cols=df$affil)
plot(bestBIC, ind_cols=df$affil)

## save PC scores to dataframe and persist to JSON
scores <- data.frame(bestBIC$scores)
results <- cbind(profiles, scores)
write.csv(results, paste("pca_scores_author_profiles_", today, ".csv", sep=""))

## save best BIC model to csv
write.csv(bestBIC$model_par$B, paste("pca_loadings_", today, ".csv", sep=""))
write.csv(bestBIC$model_par$Sigma, paste("pca_covariance_matrix_", today, ".csv", sep=""))
write.csv(bestBIC$model_par$Theta, paste("pca_fitted_theta_", today, ".csv", sep=""))
write.csv(bestBIC$eig, paste("pca_eigenvalues_", today, ".csv", sep=""))