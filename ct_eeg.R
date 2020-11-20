library(lme4)
library(effects)
library(car)
library(emmeans)
library(ggplot2)
library(knitr)
library(kableExtra)

emm_options(pbkrtest.limit = 8655)
options(width=120)
options(contrasts=c("contr.Sum","contr.Helmert"))
options(decorate.contr.Sum="",decorate.contrasts=c("[","]"))

dat <- read.csv('Cognitive Training/time_freq/alpha_theta_combined.csv')

alpha.electrodes <- c('O1', 'O2', 'Oz', 'P3', 'P4', 'Pz')

# Create O- and P-Group conditions
dat$region <- 'O-Group'
dat[dat$ch_name %in% c('P3', 'P4', 'Pz'), 'region'] <- 'P-Group'
dat$region <- as.factor(dat$region)
levels(dat$region)

dat$cond <- as.factor(dat$cond)
levels(dat$cond)

dat$session <- as.factor(dat$session)
levels(dat$session)

dat$band <- as.factor(dat$band)
levels(dat$band)

# O-Group model
dat.o.alpha.slice <- subset(dat, region == 'O-Group' & win == 'slice' & band == 'alpha')
m.o.a <- lmer(scale(power) ~ scale(epoch) * cond * iaf  + (1 | pid),
              data = dat.o.alpha.slice,
              REML = FALSE,
              na.action = na.omit,
              control=lmerControl(optimizer="bobyqa", calc.derivs=TRUE))
summary(m.o.a)

a.o.a <- Anova(m.o.a)
a.o.a

out <- capture.output(
  kable(a.o.a,
        caption = "Analysis of deviance table for alpha power mixed model. All fixed and interaction effects
        are shown, along with the Type II Wald chi-square tests and $p$-value.",
        digits = 2,
        format = "latex",
        booktabs = T) %>%
    kable_styling(latex_options = c("striped", "hold_position"),
                  full_width = F)
)
# cat(out, file="tables/tab.alpha.anova.tex", sep="n", append=FALSE)
ae.m.o <- Effect(mod = m.o.a, c('cond', 'epoch'))
ae.m.df <- as.data.frame(ae.m.o)

o.plot <- ggplot(ae.m.df, aes(x=epoch, y=fit, group=cond)) +
  geom_ribbon(aes(ymin=fit-se, ymax=fit+se), alpha = 0.1, fill = "grey70") +
  geom_line(aes(colour=cond), alpha = 1) +
  theme_light() +
  theme(text=element_text(size=10,  family="serif")) +
  labs(title="Alpha power response over time", x="Epoch", y = "Alpha Power", color="Condition")
o.plot

# O-Group model
dat.o.theta.slice <- subset(dat, region == 'O-Group' & win == 'slice' & band == 'theta')
m.o.t <- lmer(scale(power) ~ scale(epoch) * cond  + (1 | pid),
              data = dat.o.theta.slice,
              REML = FALSE,
              na.action = na.omit,
              control=lmerControl(optimizer="bobyqa", calc.derivs=TRUE))
summary(m.o.t)

a.o.t <- Anova(m.o.t)
a.o.t

out <- capture.output(
  kable(a.o.t,
        caption = "Analysis of deviance table for theta power mixed model. All fixed and interaction effects
        are shown, along with the Type II Wald chi-square tests and $p$-value.",
        digits = 2,
        format = "latex",
        booktabs = T) %>%
    kable_styling(latex_options = c("striped", "hold_position"),
                  full_width = F)
)
# cat(out, file="tables/tab.alpha.anova.tex", sep="n", append=FALSE)
ae.m.o <- Effect(mod = m.o.t, c('cond', 'epoch'))
ae.m.df <- as.data.frame(ae.m.o)

o.plot <- ggplot(ae.m.df, aes(x=epoch, y=fit, group=cond)) +
  geom_ribbon(aes(ymin=fit-se, ymax=fit+se), alpha = 0.1, fill = "grey70") +
  geom_line(aes(colour=cond), alpha = 1) +
  theme_light() +
  theme(text=element_text(size=10,  family="serif")) +
  labs(title="Theta power response over time", x="Epoch", y = "Theta Power", color="Condition")
o.plot
