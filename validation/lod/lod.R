options(menu.graphics=FALSE)
options(repos=structure(c(CRAN="http://cran.ma.imperial.ac.uk/")))

requirements<-c("reshape2","ggplot2")

for (r in requirements) {
  print(r)
  if (!(r%in%installed.packages())) {
    install.packages(r,dependencies=TRUE)
  }
}
lapply(requirements, require, character.only = TRUE)


lod<-function(inputfile) {
    # read data table
    data<-read.table(inputfile,row.names=1)
    # remove variants with low frequency overall (noise)
    data.filtered<-data[apply(data,1,function(x) max(x,na.rm=T))>0.05,]
    # remove rows with more than half missing values
    min.values<-floor(ncol(data.filtered)/2)
    row.values<-apply(data.filtered,1, function(x) length(na.omit(x)))
    data.filtered<-data.filtered[which(min.values<row.values),]
    # name columns by proportion of sample2
    steps<-seq(0,ncol(data.filtered)-1)/(ncol(data.filtered)-1)
    colnames(data.filtered)<-steps
    # impute values according to linear model
    imputed<-data.frame()
    for (r in 1:nrow(data.filtered)) {
        # build lin model
        linmod<-lm(as.numeric(data.filtered[r,]) ~ steps)
        reversed<-FALSE
        # check which sample is dominant and reverse
        if (linmod$coefficients[2]<0) {
            # reverse if negative slope
            data.filtered[r,]<-rev(data.filtered[r,])
            linmod<-lm(as.numeric(data.filtered[r,]) ~ steps)
            reversed<-TRUE
        }
        # fix lm to positive intercept
        if (linmod$coefficients[1]<0) {
            linmod<-lm(as.numeric(data.filtered[r,]) ~ steps + 0)
        }
        p<-as.numeric(predict(linmod,data.frame(x=steps)))
        # min/max from imputation if any value inputed
        rowmin<-min(min(p),min(data.filtered[r,]),na.rm=T)
        rowmax<-max(max(p),max(data.filtered[r,]),na.rm=T)
        variant<-rownames(data.filtered)[r]
        alen<-nchar(strsplit(variant,":")[[1]][3:4])
        vartype<-ifelse(alen[1]==1 & alen[2]==1,"SNV",
                ifelse(alen[1]==1 && alen[2]>1,"INS",
                ifelse(alen[1]>1 && alen[2]==1,"DEL","OTHER")))
        for (c in 1:ncol(data.filtered)) {
            imputed<-rbind(imputed, data.frame(
                variant=variant,
                vartype=vartype,
                dilution=colnames(data.filtered)[c],
                reversed=reversed,
                imputed=ifelse(is.na(data.filtered[r,c]), TRUE, FALSE),
                intercept=linmod$coefficients['steps'],
                value=ifelse(is.na(data.filtered[r,c]),p[c],data.filtered[r,c]),
                min=rowmin,
                max=rowmax))
        }
    }
    #conversions
    imputed[,"dilution"]<-as.numeric(imputed[,"dilution"])
    imputed
}


args<-commandArgs(trailingOnly = TRUE)
data<-lod(args[1])
save.image("lod.RData")

# example plots
# Consider removing low DP variants before proessing
# ggplot(data[which(data$min<0.1),]) + geom_boxplot(aes(imputed,value))
# ggplot(data[which(data$min<0.1),]) + geom_line(aes(variant,value,color=imputed))

