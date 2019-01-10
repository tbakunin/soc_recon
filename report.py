import os
from operator import itemgetter

import fpdf


def gen_report(target, rep):
    print("[=] Creating PDF...")

    class PPDF(fpdf.FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", style="I", size=8)
            self.cell(0, 10, "soc_recon report", align="C")

    pdf = PPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/TTF/DejaVuSansCondensed.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    for k in rep.keys():
        mc = sorted(rep[k], key=itemgetter(1), reverse=True)[0]
        pdf.cell(0, 10,
                 "User %s is connected to %s with ID %s. Probability is %s" % (target, k, mc[0], mc[1]),
                 border=0, ln=1)
    if "reports" not in os.listdir("."):
        os.mkdir("reports")
    os.chdir("reports")
    pdf.output(str(target) + "_report.pdf")
    os.chdir("..")
    print("[+] Done")
