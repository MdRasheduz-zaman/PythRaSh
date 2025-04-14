# make result chunks green via styles.css
knitr::opts_chunk$set(class.output = "custom-output")

# get formatted p-values from anova
getp <- function(ANOVA, term, escape_asterisks = TRUE) {
  tab <- broom::tidy(ANOVA) %>%
    mutate(p_val = insight::format_p(p.value, stars = TRUE)) %>% 
    suppressWarnings()
  
  vec <- set_names(x = tab$p_val, nm = tab$term)
  
  # Check if asterisks should be escaped
  if (escape_asterisks) {
    # Escape asterisks
    return(gsub("*", "\\*", vec[[term]], fixed = TRUE))
  } else {
    return(vec[[term]])
  }
}