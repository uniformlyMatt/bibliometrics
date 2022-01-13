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

profiles <- read_excel("../PCA_inputs_jan12.xlsx")

counts <- profiles[c(
  'citation_count',
  'cited_by_count',
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
  'SJR_median',
  'journal_h_index_median',
  'author_count_median',
  'median_citations_per_doc',
  'chw_author_position_median',
  'author_weight_median',
  'Auid',
  'affil'
)]

df <- prepare_data(counts=counts, covariates=covariates)

PCAmodels <- PLNPCA(
  Abundance ~ 1 + offset(log(Offset)) + mean_citations_per_year + growth_rate +
    SJR_median + journal_h_index_median + author_count_median +
    median_citations_per_doc + chw_author_position_median + author_weight_median,
  data=df,
  ranks=1:10
)

bestICL <- getBestModel(PCAmodels, "ICL")
bestBIC <- getBestModel(PCAmodels, "BIC")
plot(bestICL, ind_cols=df$affil)
plot(bestBIC, ind_cols=df$affil)

# save best BIC model to csv
write.csv(bestBIC$model_par$B, paste("pca_loadings_", today, ".csv", sep=""))
write.csv(bestBIC$model_par$Sigma, paste("pca_covariance_matrix_", today, ".csv", sep=""))
write.csv(bestBIC$model_par$Theta, paste("pca_fitted_theta_", today, ".csv", sep=""))
write.csv(bestBIC$eig, paste("pca_eigenvalues_", today, ".csv", sep=""))