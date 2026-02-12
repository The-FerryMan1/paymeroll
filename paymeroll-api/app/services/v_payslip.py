def calculate_deductions(basic_salary: float):
    gross_pay = basic_salary

    sss_ee = gross_pay * 0.05
    sss_er = gross_pay * 0.10

    ph_ee = gross_pay * 0.025
    ph_er = gross_pay * 0.025

    pagibig_ee = min(gross_pay * 0.02, 200.0)
    pagibig_er = min(gross_pay * 0.02, 200.0)

    taxable_income = gross_pay - (sss_ee + ph_ee + pagibig_ee)
    withholding_tax = max(0, (taxable_income - 20833) * 0.15)

    net_pay = gross_pay - (sss_ee + ph_ee + pagibig_ee + withholding_tax)

    return round(gross_pay), round(sss_ee), round(sss_er), round(ph_ee), round(ph_er), round(pagibig_ee), round(pagibig_er), round(taxable_income), round(withholding_tax), round(net_pay)
