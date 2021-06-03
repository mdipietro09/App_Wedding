
import numpy as np


class Model():

    def __init__(self, dtf, capacity=10, n_iter=10):
        self.n_tables = int(np.ceil( len(dtf)/capacity ))
        self.dic_tables = {i:capacity for i in range(self.n_tables)}
        self.dtf = dtf
        self.n_iter = n_iter


    @staticmethod
    def evaluate(dtf):
        score = 0
        for t in dtf["table"].unique():
            dtf_t = dtf[dtf["table"]==t]

            ## check penalties
            for i in dtf_t[~dtf_t["avoid"].isna()]["avoid"].values:
                if i in dtf_t["id"].values:
                    score -= 1

            ## check rewards
            seats = dtf_t["id"].values
            for n,i in enumerate(seats):
                cat = dtf_t[dtf_t["id"]==i]["category"].iloc[0]

                next_i = seats[n+1] if n < len(seats)-1 else seats[0]
                next_cat = dtf_t[dtf_t["id"]==next_i]["category"].iloc[0]
                if cat == next_cat:
                    score += 1

                prev_i = seats[n-1] if n > 0 else seats[-1]
                prev_cat = dtf_t[dtf_t["id"]==prev_i]["category"].iloc[0]
                if cat == prev_cat:
                    score += 1

        return score


    def run(self):
        best_dtf = self.dtf.copy()
        best_dtf["table"] = np.random.randint(low=1, high=self.n_tables+1, size=len(self.dtf))
        best_score = self.evaluate(best_dtf)

        for i in range(self.n_iter):
            self.dtf["table"] = np.random.randint(low=1, high=self.n_tables+1, size=len(self.dtf))
            score = self.evaluate(self.dtf)
            best_dtf = self.dtf if score > best_score else best_dtf

        return best_dtf

