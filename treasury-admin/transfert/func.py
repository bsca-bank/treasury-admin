def pct_dossier(self, entries):
    montant_tot = 0
    montant_tot_lc = 0
    tag_lc = 0
    # iterate through entries
    for entry in entries:

        if not entry.ccy == self.ccy:
            tag_lc = 1
            
            if not entry.montant_lc or entry.montant_lc == 0:
                return "LC Requis"

            montant = entry.montant
            montant_lc = entry.montant_lc

        else:
            montant = entry.montant
            montant_lc = 0

        montant_tot += montant
        montant_tot_lc += montant_lc

    if tag_lc == 0:
        pct = montant_tot / self.montant
    else:
        pct = montant_tot_lc / self.montant_lc
    return "{:.2%}".format(pct)


def pct_dom_dossier_multi(self, entries):
    montant_tot = 0
    montant_tot_lc = 0
    tag_lc = 0

    # iterate through entries
    for entry in entries:

        if not entry.ccy == self.dossier_trf.ccy:
            tag_lc = 1

            if not entry.montant_lc or entry.montant_lc == 0:
                return "LC Requis"

            montant = entry.montant
            montant_lc = entry.montant_lc

        else:
            montant = entry.montant
            montant_lc = 0

        montant_tot += montant
        montant_tot_lc += montant_lc

    if tag_lc == 0 and montant_tot > 0:
        pct = float(self.dossier_trf.montant) * float(self.dom_pct) / float(montant_tot)
        return "{:.2%}".format(pct)

    elif tag_lc == 1 and montant_tot_lc > 0:

        if not self.dossier_trf.montant_lc:
            return "LC Requis"
        else:
            pct = float(self.dossier_trf.montant_lc) * float(self.dom_pct) / float(montant_tot_lc)
            return "{:.2%}".format(pct)

    else:
        return ("ERR: (" + \
                "tag_lc: "  + str(tag_lc) + " " \
                "montant_tot: " + str(montant_tot) + " " \
                "montant_tot_lc: " + str(montant_tot_lc) 
                )    

