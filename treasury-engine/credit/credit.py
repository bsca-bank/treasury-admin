from decimal import Decimal

import numpy as np


class Credit:
    """Respresentation of the TermLoan's Amortization Table.

    Attributes:
        nominal_amount (Decimal): Asset purchase price in dollars, no cents.
        annual_interest_rate (Decimal): Yearly value growth rate of the asset.
        payment_freq (int): Yearly property tax rate as a % of
            the asset value.
        month_grace_period (int): Yearly cost of maintenance
            as a % of the asset value.
        amortization_type (Decimal): Yearly cost of insurance as
            a % of the asset value.
        tax_rate (Decimal): Yearly cost of insurance as
            a % of the asset value.
    """

    def __init__(self, principal, interest_rate, nb_year, nb_payments_year,
                 grace_period_in_month, amortization_type,tax_rate):

        self.principal = principal
        self.interest_rate = interest_rate/100
        self.nb_year = nb_year
        self.nb_payments_year = nb_payments_year
        self.grace_period_in_month = grace_period_in_month
        self.amortization_type = amortization_type
        self.tax_rate = tax_rate/100

    def get_pmt(self, year):
        """Return XXX.
        Args:
            year (int): Number of years after the purchase of the asset.
        Returns:
            Decimal: Future value of the asset.
        """
        principal = self.principal
        interest_rate = self.interest_rate
        nb_payments_year = self.nb_payments_year
        years = self.nb_year

        return Decimal(np.pmt(interest_rate/nb_payments_year,years*nb_payments_year,principal))

    def get_ipmt(self, period):
        """Return XXX.
        Args:
            year (int): Number of years after the purchase of the asset.
        Returns:
            Decimal: Future value of the asset.
        """
        principal = self.principal
        interest_rate = self.interest_rate
        nb_payments_year = self.nb_payments_year
        years = self.nb_year

        return Decimal(np.ipmt(interest_rate/nb_payments_year,period,years*nb_payments_year,principal))

    def get_ppmt(self, period):
        """Return XXX.
        Args:
            year (int): Number of years after the purchase of the asset.
        Returns:
            Decimal: Future value of the asset.
        """
        principal = self.principal
        interest_rate = self.interest_rate
        nb_payments_year = self.nb_payments_year
        years = self.nb_year

        return Decimal(np.ppmt(interest_rate/nb_payments_year,period,years*nb_payments_year,principal))

    def get_amortization_schedule(self):
        """Return XXX.
        Args:
            year (int): Number of years after the purchase of the asset.
        Returns:
            Decimal: Future value of the asset.
        """
        period = 1

        principal_t0 = self.principal
        principal_t1 = self.principal
        interest_rate = self.interest_rate
        nb_payments_year = self.nb_payments_year
        amortization_type = self.amortization_type
        grace_period = self.grace_period_in_month
        nb_year = self.nb_year

        tax_rate = self.tax_rate
        amortization_schedule = []

        pmt_constant = abs(round(np.pmt(interest_rate/nb_payments_year,nb_year*nb_payments_year,principal_t0),0))
        ppmt_constant = abs(round(principal_t0/(nb_year * nb_payments_year), 0))
        addl_principal = 0

        while principal_t1 > 0:

            ipmt = round((interest_rate/nb_payments_year)*principal_t0,0)
            tpmt = round(ipmt*tax_rate,0)

            if period <= grace_period:
                pmt = ipmt
            elif amortization_type == 1:
                pmt = pmt_constant
            else:
                pmt = ppmt_constant + ipmt + tpmt

            ppmt = pmt - ipmt - tpmt

            #ensure additional payment gets adjusted if loan is being paid off
            if principal_t1 - ppmt < ppmt/2:
                addl_principal = principal_t1 - ppmt
                ppmt = ppmt + addl_principal
                pmt = ppmt + ipmt

            principal_t1 = principal_t0 - ppmt

            # Append
            amortization_dict = {
                'period': period,
                'principal_t0': principal_t0,
                'principal_t1': principal_t1,
                'pmt': pmt,
                'ppmt': ppmt,
                'ipmt': ipmt,
                'tpmt': tpmt,
            }
            amortization_schedule.append(amortization_dict)

            #increment the counter
            period += 1
            principal_t0 = principal_t1

        return amortization_schedule
