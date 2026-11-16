"""Contract rendering for the supplied lease form.

The source document is kept unchanged.  English and Kazakh entries translate
the same numbered paragraphs, while blank runs stay as editable fields.
"""

from pathlib import Path
import re


SOURCE_DOCX = Path(__file__).with_name("contract_source.docx")

# Paragraph indexes match the paragraphs in contract_source.docx.  Keeping the
# source DOCX as the Russian master preserves its paragraph order and spacing.
PARAGRAPHS_EN = {
    0: "LEASE AGREEMENT No ________",
    1: "for non-residential premises",
    3: "“____” ________________ 20___                         City __________",
    5: "Individual Entrepreneur “_______________”, represented by {{landlord_representative_name}}, IIN _______________, registered at: _______________, notice of commencement of activity as an individual entrepreneur No. _______________ dated ____________ year, hereinafter referred to as the “Lessor”, and the “Lessee” “_______________”, IIN _______________, address: _______________, represented by director {{tenant_representative_name}}, on the other hand, jointly referred to as the “Parties”, have entered into this lease agreement for non-residential premises (the “Agreement”) and agreed as follows:",
    7: "1. SUBJECT MATTER AND SPECIAL TERMS",
    8: "1.1. The Lessor grants the Lessee temporary possession and use for consideration (lease) of non-residential premises with a total area of ___ (_________________) square metres (the “Premises”) and the constructed second floor, located at ___________________________ (the “Building”) and owned by the Lessor. The Lessee shall timely pay rent and comply with the other terms of this Agreement.",
    9: "1.2. From the date the Lessee actually occupies the Premises, the risk of accidental loss, damage or deterioration of the Premises and/or property located therein, as well as the costs of maintaining the Premises—including utilities, operating services, security and routine repairs—shall pass from the Lessor to the Lessee.",
    10: "1.3. If any licences and/or permits are required for the Lessee’s activities at the Premises, the Lessee shall obtain them independently in accordance with the applicable laws of the Republic of Kazakhstan.",
    11: "1.4. The Building’s maintenance and operation, as well as the organisation of utility services, are carried out by the operating organisation (management company).",
    12: "1.5. The Premises are provided for the purpose of {{property_use}}.",
    13: "1.6. After the Lessor receives the technical passport for the Premises, including the second floor, the area of the Premises shall be the area stated in that passport; this shall not affect the rent amount.",
    15: "2. LEASE TERM",
    16: "2.1. The Parties shall formalise the Lessor’s transfer of the Premises into the Lessee’s temporary possession and use (lease) by signing an Acceptance and Transfer Certificate for the Premises.",
    17: "2.2. If the Lessee refuses to sign the Acceptance and Transfer Certificate, rent shall be payable from the date the Lessee actually occupies the Premises.",
    18: "2.3. The term of this Agreement is 11 (eleven) months.",
    19: "2.4. Throughout the term of this Agreement, the Lessee may not sublease, pledge, assign the lease right to third parties, make the Premises wholly or partly available to third parties, or transfer its rights or obligations under this Agreement to third parties on any grounds without the Lessor’s prior written consent. If the Lessor permits subleasing, the rent may be increased.",
    20: "2.5. At the end of this Agreement, subject to the Parties’ mutual consent, the Parties may enter into a new lease agreement for a new term on new terms. The Lessee shall send the Lessor a letter expressing its intention to renew at least 30 (thirty) calendar days before the current lease term expires.",
    21: "2.6. Upon expiry of the lease term or termination of this Agreement on any other grounds, the Lessee shall vacate and return the Premises to the Lessor within 10 (ten) calendar days, allowing for normal wear and tear. The return shall be documented by a Premises Return Certificate. From the date it is signed by the Parties, the certificate forms an integral part of this Agreement and confirms that the Lessee has actually returned the Premises to the Lessor.",
    23: "SECTION 3. RENT AND OTHER PAYMENTS",
    24: "3.1. The monthly rent for possession and use (lease) of the Premises is: through ______________ year (inclusive) — ________________ tenge; from ____________ year until the end of the Agreement — ________________ tenge.",
    25: "3.2. Rent shall be charged to the Lessee starting from _____________ year. The Parties acknowledge that the Lessee actually occupied the Premises on _________ year. The Lessee was exempt from rent for the period from _____________ year to _____________ year because the Lessee incurred expenses for finishing repairs to the Premises. The Lessor allowed the Lessee to carry out repairs at its discretion, suitable for the provision of cosmetology services. The Parties agree that the Lessor will not reimburse the Lessee for the cost of these improvements (finishing repairs) when the Agreement expires or is terminated on any grounds.",
    26: "3.3. Rent shall be paid monthly in advance within the first three business days of the month being paid for. Rent stops accruing on the date the Lessee actually vacates and returns the Premises to the Lessor under the Premises Return Certificate.",
    27: "3.4. The Lessee shall make monthly rent payments in the amounts and by the deadlines set out in this Agreement.",
    28: "3.5. The rent specified in clause 3.1 does not include the cost of maintaining, servicing or operating the Premises (operating expenses), utilities—including, without limitation, hot and cold water, sewerage, electricity and heating—security, cleaning, intercom maintenance or other services.",
    29: "3.6. Rent does not include local, long-distance or international telephone services, Internet or cable television.",
    30: "3.7. The Lessee shall pay the cost of utilities to the Lessor within five business days after the relevant invoices are presented.",
    31: "3.8. The Parties shall share equally the costs of obtaining a technical passport and other identification documents for the Premises, which in fact consist of two floors.",
    33: "SECTION 4. EARLY TERMINATION",
    34: "4.1. The Lessor may terminate this Agreement early and unilaterally if the Lessee breaches a material term of the Agreement. A material breach includes any of the following:",
    35: "4.1.1. the Lessee is 15 (fifteen) calendar days late in performing any monetary obligation under the Agreement;",
    36: "4.1.2. the Lessee uses the Premises for purposes not provided for in this Agreement without the Lessor’s written consent;",
    37: "4.1.3. the Lessee repeatedly (two or more times) breaches any obligation assumed under this Agreement;",
    38: "4.1.4. the Lessee refuses or evades signing the Acceptance and Transfer Certificate for the Premises.",
    39: "4.2. In the cases specified in clause 4.1, the Lessor shall send the Lessee written notice of termination no later than 5 (five) calendar days before the termination date. A separate written termination agreement is not required. The Agreement terminates 5 (five) calendar days after the Lessee receives the notice. The Lessee shall vacate and return the Premises to the Lessor, pay any outstanding rent and other payments, and pay any penalty due under this Agreement.",
    40: "4.3. The Lessor and the Lessee may terminate this Agreement early at any time by mutual consent.",
    41: "4.4. In the case specified in clause 4.3, the initiating Party shall notify the other Party of termination at least 30 (thirty) calendar days before the termination date. A separate written termination agreement is not required. The Agreement terminates 30 (thirty) calendar days after the other Party receives the notice. The Lessee shall vacate and return the Premises and pay any outstanding rent and other payments, if any.",
    43: "SECTION 5. RIGHTS AND OBLIGATIONS OF THE LESSEE",
    44: "5.1. The Lessee shall:",
    45: "5.1.1. If the Premises or property located therein or in common areas is damaged through the fault of the Lessee’s employees, third parties engaged by the Lessee, or visitors, repair (restore) the damage within 10 (ten) business days after receiving the Lessor’s written request (the Parties may extend this period depending on the nature of the repairs), or reimburse the Lessor for documented losses related to the damage, in accordance with the laws of the Republic of Kazakhstan;",
    46: "5.1.2. Throughout the lease term, keep the Premises in good condition and at its own expense perform routine repairs (remedying defects in the Premises, its components, systems, engineering equipment and finishes that are not capital repairs) and improvements, including through third parties, without damaging load-bearing structures, walls or utilities, including heating, sewerage, electricity, water supply and telephone lines;",
    47: "5.1.3. Treat the Premises with care (do not scratch floors or walls with furniture; open and close windows and doors carefully);",
    48: "5.1.4. Treat with care the property in the Premises and in common areas, including heating and lighting fixtures, bathrooms and other property;",
    49: "5.1.5. Observe fire-safety rules and rules for using heat and electricity, and do not overload electrical networks;",
    50: "5.1.6. Keep the Premises in proper sanitary condition;",
    51: "5.1.7. Not rebuild or re-plan the Premises without the Lessor’s written consent;",
    52: "5.1.8. Within 5 (five) calendar days after this Agreement ends, remove its property and any property brought into the Premises during the lease, and return the Premises to the Lessor under a Premises Return Certificate in condition suitable for further use, allowing for normal wear and tear;",
    53: "5.1.9. Bear the risks associated with damage to or loss of its property located in the Premises, regardless of the circumstances that caused the damage or loss;",
    54: "5.1.10. Make any improvements to the Premises (including installing air conditioners or other equipment) only after obtaining the Lessor’s written consent;",
    55: "5.1.11. Independently bear the costs of installing security, fire and other alarm systems and video surveillance;",
    56: "5.1.12. Technical equipment installed and connected by the Lessee that can be removed without damaging the leased Premises remains the Lessee’s property. The Parties agree that installing an air conditioner is an inseparable improvement;",
    57: "5.1.13. Immediately take all necessary measures to address any emergency and notify the Lessor;",
    58: "5.1.14. Provide utility, operating and other service representatives free access to water, sewerage and other plumbing, electrical and telephone equipment;",
    59: "5.1.15. Not install equipment in the Premises without the Lessor’s consent;",
    60: "5.1.16. Independently bear the costs of repairs or re-equipping needed to bring the Premises into compliance with applicable laws governing the Lessee’s business activities.",
    62: "5.2. The Lessee may:",
    63: "5.2.1. Use the utility systems located in the Building;",
    64: "5.2.2. Equip and decorate the Premises at its discretion and identify its location there by placing signs or information boards at the entrance, using a design approved in advance by the Lessor and after obtaining any required permit from the competent authority. The Lessee is responsible for obtaining documents and permits and for the costs of installing signs, boards and advertising structures;",
    65: "5.2.3. Install alarm systems and other security systems for the Premises in coordination with the Lessor;",
    66: "5.2.4. Require the prompt remedy of faults and inconveniences caused by the Lessor;",
    67: "5.2.5. Take any action related in any way or form to this Agreement, but not expressly provided for in it, only with the Lessor’s written consent;",
    68: "5.2.6. Exercise other rights provided for in this Agreement and the laws of the Republic of Kazakhstan.",
    69: "5.3. The Lessee must not:",
    70: "5.3.1. Pour or discharge flammable liquids, acids, household or construction waste or other items that clog drains into sewerage networks or other sanitary equipment;",
    71: "5.3.2. Independently adjust heat supply at the heating unit or install additional heating sections;",
    72: "5.3.3. Obstruct or alter fire exits, store radioactive, flammable or explosive materials in common areas, or store substances that pollute the air;",
    73: "5.3.4. Install or connect additional equipment without the Lessor’s written consent;",
    74: "5.3.5. Install or connect equipment that has no technical passport (certificate) or does not meet operational-safety and sanitary-hygiene requirements;",
    75: "5.3.6. Make changes to existing structural elements of the Premises specified in the construction design that affect load-bearing or enclosing structures (foundations, bases, frames, columns, shear walls, load-bearing walls, floors, reinforcement or utility networks); affect existing ventilation units; or drill holes without first checking the location of engineering utilities in the walls and other structures, including electrical networks;",
    76: "5.3.7. Clutter common areas with the Lessee’s property;",
    77: "5.3.8. Permit smoking in the Premises or common areas (lobbies, stairwells, lifts, corridors, etc.).",
    79: "SECTION 6. RIGHTS AND OBLIGATIONS OF THE LESSOR",
    80: "6.1. The Lessor shall:",
    81: "6.1.1. Transfer the Premises to the Lessee under an Acceptance and Transfer Certificate and ensure the Lessee can use the Premises without obstruction under the terms of this Agreement;",
    82: "6.1.2. Ensure the engineering systems of the Premises operate continuously, including uninterrupted cold and hot water and electricity. The Lessor is not liable for a failure to supply water, heat or electricity caused by an accident on municipal heating or power networks;",
    83: "6.1.3. Provide the Lessee with information about the operating organisation (management company) that manages, services and operates the Premises.",
    84: "6.2. The Lessor may:",
    85: "6.2.1. During any business hours and without notifying the Lessee, inspect how the Lessee uses the Premises, draw up an inspection report recording any deficiencies or comments, and set a deadline for remedying them;",
    86: "6.2.2. Exercise other rights under this Agreement, including, without limitation, early termination in the cases provided for herein, requiring the Lessee to sign the Acceptance and Transfer Certificate, applying the sanctions in section 7 if the Lessee breaches its obligations, and refusing to enter into a new agreement for a new term.",
    88: "SECTION 7. LIABILITY OF THE PARTIES",
    89: "7.1. The Lessee is fully responsible for compliance with fire and electrical safety rules and for proper operation of technical equipment and engineering systems in the Premises, as well as for the consequences of non-compliance. The Lessee is responsible for all persons it engages to perform work or allows access to the Building’s engineering networks, including its employees, visitors, contractors and other counterparties.",
    90: "7.2. If rent and/or utility costs are paid late, the Lessee shall, at the Lessor’s request, pay a penalty of 0.5% of the overdue amount for each day of delay.",
    91: "7.3. The Lessor is not liable to the Lessee for loss or damage resulting from theft of or damage to any of the Lessee’s property located in the Premises or car park, or for the safety of valuables, personal property or other property there.",
    92: "7.4. The Lessor is not liable for the Lessee’s property or other inventory stored in the Premises; the Lessee independently takes measures to keep it safe.",
    93: "7.5. The Lessor is not liable for actions of third parties that cause the Premises to become unsafe, interrupt utilities or damage the Lessee’s equipment or other property.",
    94: "7.6. If the Lessee is more than 30 (thirty) calendar days late in paying rent or other payments under this Agreement, the Lessor may, after giving the Lessee prior written notice, disconnect electricity to the Premises and prohibit the Lessee’s representatives and employees from entering the Premises (restrict access).",
    95: "The Lessor is not liable for any damage or losses that may be caused to the Lessee as a result of the actions specified in this clause.",
    96: "7.7. If, after this Agreement ends, the Lessee does not vacate the Premises on time, it shall pay the Lessor:",
    97: "7.7.1. the cost of using the Premises for the entire period of delay in returning it, and operating expenses and utilities for that period;",
    98: "7.7.2. a penalty of 1% of one quarter’s rent for each day the return of the Premises is delayed, and reimburse the Lessor for losses related to the delay.",
    99: "7.8. The Lessee represents and warrants that it has all licences and other permits required by the authorities of the Republic of Kazakhstan for the activities carried out in the Premises. If a licence or permit expires, is cancelled, suspended or revoked, or is otherwise unavailable to the Lessee, the Lessee bears full independent responsibility under the laws of the Republic of Kazakhstan for carrying out its activities and using the Premises under this Agreement without the required licence or permit.",
    100: "7.9. If the Lessee delays any monetary obligation or reimbursement of expenses or damage under this Agreement, it shall pay the Lessor a penalty of 0.5% of the overdue amount for each day of delay.",
    101: "7.10. The Lessor shall not reimburse the Lessee for costs of capital repairs or finishing work carried out before operations began if this Agreement ends or is terminated on any grounds or at either Party’s initiative.",
    102: "7.11. The Lessee agrees that the Lessee’s property may be retained as security for the Lessee’s obligations under this Agreement.",
    103: "7.12. If the Lessee fails to remove any property from the Premises after the lease term expires, the Lessor may, at its discretion, remove all or part of that property by any convenient means and/or transfer it to another person for storage or leave it unattended, without liability for its safekeeping or storage costs. To secure payment of actual removal expenses, the Lessor may retain part of the property. If the Lessee does not reimburse those expenses within 3 (three) months, the Lessor may sell or otherwise dispose of the retained property to satisfy its claims, including any other debt under this Agreement. In these circumstances, the Lessee may not claim that the expenses were disproportionate to the value of the property sold.",
    104: "7.13. Payment of a penalty (fine or late fee) under this Agreement does not release the Parties from properly performing their obligations.",
    105: "7.14. The Lessee is liable for personal injury (including injury caused by falling on steps not cleared of snow or ice, an unlit staircase, improper wet cleaning or debris on the floor) and property damage resulting from the Lessee’s failure to ensure safe use of the Premises or take adequate measures to prevent accidents.",
    106: "7.15. The Lessee is liable for damage caused to the Lessor and/or third parties by emergencies arising through the Lessee’s fault.",
    107: "SECTION 8. FORCE MAJEURE",
    108: "8.1. The Parties are released from liability for failure to perform or improper performance of their obligations if performance becomes impossible due to force majeure circumstances (the “Circumstances”), such as natural disasters, wars, armed conflicts, mass civil unrest, epidemics, or extraordinary natural or man-made events, provided that they directly affect the Parties’ performance of this Agreement.",
    109: "8.2. A Party affected by force majeure shall notify the other Party in writing of the start and/or end of the Circumstances within 10 (ten) days of their start or end, stating how they affect proper performance of the Agreement. The Agreement may be suspended wholly or partly for the duration of the Circumstances. If a Circumstance continues for more than 60 (sixty) calendar days and shows no signs of ending, the Parties shall jointly determine further action and may suspend or terminate the Agreement.",
    110: "8.3. A Party that fails to notify the other Party in writing in a timely manner of the force majeure Circumstances and their effect on performance may not rely on them as grounds for release from liability for breach of its obligations.",
    112: "SECTION 9. FINAL PROVISIONS",
    113: "9.1. The Parties shall make every effort to resolve any dispute or disagreement arising out of or in connection with this Agreement amicably through out-of-court negotiations. If they cannot resolve it, the dispute shall be settled by a court. The Parties have agreed that the courts of Astana shall have jurisdiction.",
    114: "9.2. Any amendment or supplement to this Agreement is valid only if made in writing, signed by authorised representatives of the Parties and bearing their seals.",
    115: "9.3. Neither Party may transfer its rights or obligations under this Agreement to third parties without the other Party’s written consent.",
    116: "9.4. If any article or provision of this Agreement is invalid under the laws of the Republic of Kazakhstan, the Agreement as a whole remains valid. The remaining articles and provisions apply to the extent that they do not conflict with the laws of the Republic of Kazakhstan.",
    117: "9.5. This Agreement enters into force on the date it is signed and remains in effect until the Parties have fully performed their obligations.",
    118: "9.6. This Agreement is made and signed in 2 (two) original copies of equal legal effect, one for each Party.",
    120: "SECTION 10. DETAILS, SIGNATURES AND SEALS OF THE PARTIES",
    122: "Individual Entrepreneur “_______________”,",
    123: "represented by {{landlord_representative_name}},",
    124: "IIN ____________",
    125: "Address: ___________________",
    126: "IBAN: _____________",
    127: "BIC: _______________",
    128: "Telephone: ___________",
    131: "Individual Entrepreneur “_______________”,",
    132: "represented by {{tenant_representative_name}},",
    133: "IIN ____________",
    134: "Address: ___________________",
    135: "IBAN: _____________",
    136: "BIC: _______________",
    137: "Telephone: ___________",
    142: "Lessor                         Lessee",
    144: "Individual Entrepreneur {{landlord_representative_name}}/signature/             Individual Entrepreneur {{tenant_representative_name}}/signature/",
}


PARAGRAPHS_KK = {
    0: "ЖАЛҒА АЛУ ШАРТЫ № ________",
    1: "тұрғын емес үй-жайды жалға алу туралы",
    3: "«____» ________________ 20___ ж.                         Қала __________",
    5: "«_______________» Жеке кәсіпкері, {{landlord_representative_name}} тұлғасында, ЖСН _______________, мына мекенжай бойынша тіркелген: _______________, жеке кәсіпкер ретінде қызметтің басталғаны туралы № _______________ хабарлама, ____________ жылы, бұдан әрі «Жалға беруші» деп аталатын, және «Жалға алушы» «_______________», ЖСН _______________, мекенжайы: _______________, директор {{tenant_representative_name}} тұлғасында, екінші тараптан, бұдан әрі бірлесіп «Тараптар» деп аталатын, тұрғын емес үй-жайды жалға алу туралы осы шартты (бұдан әрі — Шарт) жасасты және төмендегілер туралы келісімге келді:",
    7: "1. ШАРТТЫҢ МӘНІ ЖӘНЕ АРНАЙЫ ТАЛАПТАР",
    8: "1.1. Жалға беруші Жалға алушыға уақытша иеленуге және ақылы пайдалануға (жалға алуға) жалпы ауданы ___ (_________________) шаршы метр тұрғын емес үй-жайды (бұдан әрі — Үй-жай) және салынған екінші қабатты береді. Үй-жай ___________________________ мекенжайында орналасқан (бұдан әрі — Ғимарат) және Жалға берушіге тиесілі. Жалға алушы жалдау ақысын уақтылы төлеуге және осы Шартта көзделген өзге талаптарды орындауға міндеттенеді.",
    9: "1.2. Жалға алушы Үй-жайды нақты иеленген күннен бастап Үй-жайдың және/немесе онда орналасқан мүліктің кездейсоқ жойылу, бүліну немесе бұзылу тәуекелі, сондай-ақ Үй-жайды күтіп-ұстау ауыртпалығы, оның ішінде коммуналдық және пайдалану қызметтерін, күзетті төлеу және ағымдағы жөндеу жүргізу міндеттері Жалға берушіден Жалға алушыға өтеді.",
    10: "1.3. Егер Жалға алушының Үй-жайдағы қызметін жүзеге асыру үшін қандай да бір лицензиялар және/немесе рұқсаттар қажет болса, Жалға алушы оларды Қазақстан Республикасының қолданыстағы заңнамасының талаптарына сәйкес өз бетінше алуға міндеттенеді.",
    11: "1.4. Ғимаратқа қызмет көрсетуді және оны пайдалануды, сондай-ақ коммуналдық қызметтерді ұйымдастыруды пайдаланушы ұйым (басқарушы компания) жүзеге асырады.",
    12: "1.5. Үй-жай {{property_use}} мақсатында пайдалануға беріледі.",
    13: "1.6. Жалға беруші екінші қабатты ескере отырып Үй-жайдың техникалық паспортын алғаннан кейін Үй-жайдың ауданы паспортта көрсетілген аудан болып есептеледі; бұл жалдау ақысының мөлшеріне әсер етпейді.",
    15: "2. ЖАЛҒА АЛУ МЕРЗІМІ",
    16: "2.1. Жалға берушінің Үй-жайды Жалға алушының уақытша иеленуіне және пайдалануына (жалға алуына) беруі Тараптардың Үй-жайды жалға алуға қабылдау-тапсыру актісіне қол қоюы арқылы ресімделеді.",
    17: "2.2. Жалға алушы қабылдау-тапсыру актісіне қол қоюдан бас тартқан жағдайда, жалдау ақысы Үй-жайды нақты иеленген күннен бастап төленеді.",
    18: "2.3. Осы Шарттың қолданылу мерзімі: 11 (он бір) ай.",
    19: "2.4. Осы Шарттың бүкіл қолданылу мерзімі ішінде Жалға алушы Жалға берушінің алдын ала жазбаша келісімінсіз Үй-жайды қосалқы жалға беруге, кепілге қоюға, жалдау құқығын үшінші тұлғаларға беруге, Үй-жайды толық немесе ішінара үшінші тұлғалардың пайдалануына беруге, сондай-ақ осы Шарт бойынша өз құқықтары мен міндеттерін кез келген негіз бойынша үшінші тұлғаларға беруге құқылы емес. Жалға берушінің рұқсатымен қосалқы жалға берілген жағдайда жалдау ақысының мөлшері ұлғайтылуы мүмкін.",
    20: "2.5. Осы Шарттың мерзімі аяқталған кезде Тараптардың өзара келісімі болған жағдайда, олар жаңа мерзімге жаңа талаптармен жаңа жалдау шартын жасасады. Бұл ретте Жалға алушы осы Шарт бойынша жалдау мерзімі аяқталғанға дейін 30 (отыз) күнтізбелік күннен кешіктірмей, жаңа мерзімге жалдау шартын жасасу ниеті туралы хатты Жалға берушіге жіберуге міндетті.",
    21: "2.6. Жалдау мерзімі аяқталған немесе осы Шарт өзге негіздер бойынша тоқтатылған жағдайда, Жалға алушы 10 (он) күнтізбелік күн ішінде Үй-жайды қалыпты тозуын ескере отырып босатып, Жалға берушіге қайтаруға міндетті. Үй-жайды қайтару Үй-жайды қайтару актісіне қол қою арқылы ресімделеді. Тараптар қол қойған күннен бастап акт осы Шарттың ажырамас бөлігі болып табылады және оған қол қою Үй-жайдың Жалға алушыдан Жалға берушіге нақты қайтарылғанын растайды.",
    23: "3-БӨЛІМ. ЖАЛДАУ АҚЫСЫ ЖӘНЕ ӨЗГЕ ТӨЛЕМДЕР",
    24: "3.1. Үй-жайды иеленгені және пайдаланғаны (жалға алғаны) үшін ай сайынғы жалдау ақысы: ______________ жылға дейін (қоса алғанда) — ________________ теңге, ____________ жылдан бастап Шарт мерзімі аяқталғанға дейін — ________________ теңге.",
    25: "3.2. Жалға алушыдан жалдау ақысы _____________ жылдан бастап алынады. Тараптар Үй-жайды Жалға алушының нақты иеленген күні _________ жыл болғанын растайды. Бұл ретте Жалға алушы Үй-жайды жөндеуге (әрлеу жұмыстарына) шығын шығарғанына байланысты, _____________ жылдан _____________ жылға дейінгі кезең үшін жалдау ақысын төлеуден босатылды. Жалға беруші Жалға алушыға косметологиялық қызметтер көрсету қызметіне сәйкес келетін жөндеуді өз қалауы бойынша жүргізуге рұқсат берді. Тараптар Шарт мерзімі аяқталған немесе ол кез келген негіз бойынша бұзылған жағдайда, Жалға беруші Жалға алушы жүргізген жөндеу (әрлеу жұмыстары) түріндегі жақсартулардың құнын өтемейді деп келісті.",
    26: "3.3. Жалдау ақысы ай сайын алдын ала — төленетін айдың алғашқы үш жұмыс күні ішінде төленеді және Жалға алушы Үй-жайды нақты босатып, оны қайтару актісі бойынша Жалға берушіге қайтарған күннен бастап тоқтатылады.",
    27: "3.4. Жалға алушы осы Шарт бойынша жалдау төлемдерін ай сайын Шартта көзделген мерзімдерде және мөлшерде төлеуге міндеттенеді.",
    28: "3.5. Шарттың 3.1-тармағында көрсетілген жалдау ақысына Үй-жайды күтіп-ұстау, қызмет көрсету және пайдалану құны (пайдалану шығыстары), коммуналдық қызметтер, оның ішінде ыстық және суық сумен жабдықтау, кәріз, электрмен және жылумен жабдықтау, күзет, тазалау, домофондарға қызмет көрсету және өзге де қызметтер кірмейді.",
    29: "3.6. Жалдау ақысына қалалық, қалааралық және халықаралық телефон байланысы, интернет және кабельдік теледидар қызметтерінің құны кірмейді.",
    30: "3.7. Коммуналдық қызметтердің құнын Жалға алушы тиісті шоттар ұсынылғаннан кейін бес жұмыс күні ішінде Жалға берушіге төлейді.",
    31: "3.8. Екі қабаттан тұратын Үй-жайға техникалық паспорт және өзге сәйкестендіру құжаттарын алу шығындарын Тараптар тең үлеспен көтереді.",
    33: "4-БӨЛІМ. ШАРТТЫ МЕРЗІМІНЕН БҰРЫН БҰЗУ",
    34: "4.1. Жалға алушы Шарттың елеулі талаптарын бұзған жағдайда, Жалға беруші осы Шартты біржақты тәртіппен мерзімінен бұрын бұзуға құқылы. Шарттың елеулі талаптарын бұзу деп мынадай бұзушылықтардың бірі танылады:",
    35: "4.1.1. Жалға алушының Шартта көзделген кез келген ақшалай міндеттемені орындауды 15 (он бес) күнтізбелік күнге кешіктіруі;",
    36: "4.1.2. Жалға алушының Жалға берушінің жазбаша келісімінсіз Үй-жайды осы Шартта көзделмеген мақсаттарда пайдалануы;",
    37: "4.1.3. Жалға алушының осы Шарт бойынша қабылдаған кез келген міндеттемесін жүйелі түрде (екі немесе одан көп рет) бұзуы;",
    38: "4.1.4. Жалға алушының Үй-жайды жалға алуға қабылдау-тапсыру актісіне қол қоюдан бас тартуы немесе жалтаруы.",
    39: "4.2. Осы Шарттың 4.1-тармағында көрсетілген жағдайларда Жалға беруші Шартты бұзу күніне дейін кемінде 5 (бес) күнтізбелік күн бұрын Жалға алушыға Шартты бұзу туралы жазбаша хабарлама жіберуге міндетті. Бұл ретте Шартты бұзу туралы жеке жазбаша келісім талап етілмейді. Жалға алушы хабарламаны алған күннен бастап 5 (бес) күнтізбелік күн өткен соң Шарт бұзылды деп есептеледі. Бұл ретте Жалға алушы Үй-жайды босатып, Жалға берушіге қайтаруға, жалдау ақысы және өзге төлемдер бойынша берешекті өтеуге және Шарт талаптарына сәйкес өсімпұл төлеуге міндетті.",
    40: "4.3. Жалға беруші мен Жалға алушы өзара келісім бойынша осы Шартты кез келген уақытта мерзімінен бұрын бұзуға құқылы.",
    41: "4.4. Шарттың 4.3-тармағында көрсетілген жағдайда, бастамашы Тарап Шартты бұзу күніне дейін кемінде 30 (отыз) күнтізбелік күн бұрын екінші Тарапқа бұзу туралы хабарлама жіберуге міндетті. Шартты бұзу туралы жеке жазбаша келісім талап етілмейді. Тарап хабарламаны алған күннен бастап 30 (отыз) күнтізбелік күн өткен соң Шарт бұзылды деп есептеледі. Бұл ретте Жалға алушы Үй-жайды босатып, Жалға берушіге қайтаруға және (бар болса) берешекті өтеуге міндетті.",
    43: "5-БӨЛІМ. ЖАЛҒА АЛУШЫНЫҢ ҚҰҚЫҚТАРЫ МЕН МІНДЕТТЕРІ",
    44: "5.1. Жалға алушы міндеттенеді:",
    45: "5.1.1. Жалға алушының қызметкерлерінің, ол қандай да бір жұмысқа тартқан үшінші тұлғалардың немесе Үй-жайға келген адамдардың кінәсінен Үй-жайға немесе ортақ пайдаланылатын жерлердегі мүлікке зиян келтірілген жағдайда, Жалға берушінің жазбаша талабын алған күннен бастап 10 (он) жұмыс күні ішінде бүлінген Үй-жайды қалпына келтіру (Тараптар жөндеу жұмыстарының сипатына қарай бұл мерзімді ұзартуы мүмкін) немесе Қазақстан Республикасының заңнамасына сәйкес осындай залалды растайтын құжаттар негізінде Жалға берушінің шығындарын өтеу;",
    46: "5.1.2. Жалдау мерзімі бойы Үй-жайды жарамды күйде ұстау, ағымдағы жөндеуді және жақсартуларды өз есебінен орындау, оның ішінде үшінші тұлғаларды тарту арқылы, көтергіш құрылымдарға, қабырғаларға және инженерлік желілерге (жылыту, кәріз, электр, сумен жабдықтау, телефон желілері және басқалары) зиян келтірмеу;",
    47: "5.1.3. Үй-жайға ұқыпты қарау (жиһазбен еденді және қабырғаларды сызбау, терезелер мен есіктерді ұқыпты ашып-жабу);",
    48: "5.1.4. Үй-жайда және ортақ пайдаланылатын жерлерде орналасқан мүлікке, оның ішінде жылыту және жарықтандыру аспаптарына, санитариялық тораптарға және өзге мүлікке ұқыпты қарау;",
    49: "5.1.5. Өрт қауіпсіздігі ережелерін, сондай-ақ жылу және электр энергиясын пайдалану қағидаларын сақтау, электр желілерінің шамадан тыс жүктелуіне жол бермеу;",
    50: "5.1.6. Үй-жайды тиісті санитариялық жағдайда ұстау;",
    51: "5.1.7. Жалға берушінің жазбаша келісімінсіз Үй-жайды қайта жабдықтамау және қайта жоспарламау;",
    52: "5.1.8. Осы Шарт тоқтатылғаннан кейін 5 (бес) күнтізбелік күн ішінде өз мүлкін және жалдау мерзімі кезінде Үй-жайға әкелінген мүлікті алып кету және қалыпты тозуын ескере отырып, Үй-жайды одан әрі пайдалануға жарамды күйде қайтару актісі бойынша Жалға берушіге қайтару;",
    53: "5.1.9. Үй-жайда орналасқан өз мүлкінің бүлінуіне немесе жоғалуына байланысты тәуекелдерді, зиян немесе жоғалту себептеріне қарамастан, өз мойнына алу;",
    54: "5.1.10. Үй-жайда кез келген жақсартуларды (оның ішінде кондиционерлерді және өзге жабдықты орнатуды) Жалға берушімен жазбаша келісілгеннен кейін ғана жүргізу;",
    55: "5.1.11. Күзет, өрт және өзге сигнализациялар мен бейнебақылауды орнатуға байланысты шығындарды өз бетінше көтеру;",
    56: "5.1.12. Жалға алушы орнатқан және қосқан, жалға алынған Үй-жайға зиян келтірмей алып тастауға болатын техникалық құралдар Жалға алушының меншігі болып табылады. Тараптар кондиционерді (кондиционерлерді) орнату ажырамайтын жақсарту болып табылады деп келісті;",
    57: "5.1.13. Әртүрлі авариялық жағдайлар туындаған кезде оларды жою үшін қажетті шараларды дереу қабылдау және бұл туралы Жалға берушіге хабарлау;",
    58: "5.1.14. Коммуналдық, пайдалану және өзге қызмет өкілдеріне су құбыры, кәріз және басқа сантехникалық, электр және телефон жабдықтарына еркін қол жеткізуді қамтамасыз ету;",
    59: "5.1.15. Жалға берушімен келісілмеген жабдықты Үй-жайға орнатпау;",
    60: "5.1.16. Жалға алушының қызмет саласына қатысты қолданыстағы заңнама талаптарына Үй-жайды сәйкестендіру қажет болған жағдайда жөндеу және қайта жабдықтау шығындарын өз бетінше көтеру.",
    62: "5.2. Жалға алушы құқылы:",
    63: "5.2.1. Ғимаратта орналасқан инженерлік коммуникациялар жүйелерін пайдалануға;",
    64: "5.2.2. Үй-жайды өз қалауы бойынша жабдықтауға және безендіруге, Жалға берушімен алдын ала келісілген үлгі бойынша және уәкілетті органның рұқсатын алғаннан кейін кіреберістің алдына маңдайша немесе көрсеткіш тақта орнату арқылы орналасқан жерін белгілеуге. Құжаттар мен рұқсаттарды алу Жалға алушының міндеті; маңдайшаларды, тақталарды және жарнамалық құрылымдарды орнату шығындарын Жалға алушы көтереді;",
    65: "5.2.3. Жалға берушімен келісу арқылы Үй-жайға сигнализацияның және күзеттің өзге жүйелерін орнатуға;",
    66: "5.2.4. Жалға берушінің кінәсінен туындаған ақаулар мен қолайсыздықтарды дереу жоюды талап етуге;",
    67: "5.2.5. Осы Шартпен қандай да бір дәрежеде немесе нысанда байланысты, бірақ онда тікелей көзделмеген әрекеттерді Жалға берушінің жазбаша келісімімен ғана жасауға;",
    68: "5.2.6. Осы Шартта және Қазақстан Республикасының заңнамасында көзделген өзге құқықтарды жүзеге асыруға.",
    69: "5.3. Жалға алушыға тыйым салынады:",
    70: "5.3.1. Кәріз желілері мен өзге санитариялық құрылғыларға тез тұтанатын сұйықтықтарды, қышқылдарды, тұрмыстық және құрылыс қалдықтарын және кәрізді бітейтін өзге заттарды төгуге;",
    71: "5.3.2. Жылу торабында жылу беруді өз бетінше реттеуге және жылыту аспаптарының қосымша секцияларын орнатуға;",
    72: "5.3.3. Өртке қарсы өтетін жолдарды заттармен бөгеуге немесе қайта құруға, ортақ пайдаланылатын жерлерде радиоактивті, өрт қауіпті және жарылғыш материалдарды, сондай-ақ ауаны ластайтын заттарды сақтауға;",
    73: "5.3.4. Жалға берушімен жазбаша келіспей қосымша жабдықты орнатуға немесе қосуға;",
    74: "5.3.5. Техникалық паспорттары (куәліктері) жоқ немесе пайдалану қауіпсіздігі мен санитариялық-гигиеналық нормаларға сәйкес келмейтін жабдықты орнатуға немесе қосуға;",
    75: "5.3.6. Құрылыс жобасында көзделген Үй-жайдың қолданыстағы конструкциялық шешімдерін өзгертуге, оның ішінде көтергіш немесе қоршау конструкцияларына (іргетастарға, негіздерге, қаңқаға, бағандарға, қаттылық диафрагмаларына, көтергіш қабырғаларға, жабындарға, арматураға, инженерлік желілерге және басқаларға) әсер ететін өзгерістер енгізуге, қолданыстағы желдету блоктарын өзгертуге, сондай-ақ қабырғалар мен өзге конструкциялардан өтетін инженерлік коммуникациялардың, оның ішінде электр желілерінің орналасқан жерін алдын ала анықтамай тесік бұрғылауға;",
    76: "5.3.7. Ортақ пайдаланылатын жерлерді Жалға алушының мүлкімен бөгеуге;",
    77: "5.3.8. Үй-жайда және ортақ пайдаланылатын жерлерде (вестибюльдерде, баспалдақ алаңдарында, лифтілерде, дәліздерде және т.б.) темекі шегуге жол беруге.",
    79: "6-БӨЛІМ. ЖАЛҒА БЕРУШІНІҢ ҚҰҚЫҚТАРЫ МЕН МІНДЕТТЕРІ",
    80: "6.1. Жалға беруші міндеттенеді:",
    81: "6.1.1. Үй-жайды жалға алуға қабылдау-тапсыру актісі бойынша Жалға алушыға беруге және осы Шарт талаптарына сәйкес Үй-жайды кедергісіз пайдалануды қамтамасыз етуге;",
    82: "6.1.2. Үй-жайдың инженерлік жүйелерінің үздіксіз жұмысын, оның ішінде суық және ыстық сумен, электр энергиясымен үздіксіз жабдықтауды қамтамасыз етуге. Қалалық жылу немесе энергия желілерінде авария болған жағдайда Жалға беруші Үй-жайды сумен, жылумен және электр энергиясымен қамтамасыз етпеу үшін жауап бермейді;",
    83: "6.1.3. Үй-жайды басқаруды, қызмет көрсетуді және пайдалануды жүзеге асыратын пайдаланушы ұйым (басқарушы компания) туралы Жалға алушыға ақпарат беруге.",
    84: "6.2. Жалға беруші құқылы:",
    85: "6.2.1. Кез келген жұмыс уақытында Жалға алушыға хабарламай Үй-жайдың қалай пайдаланылып жатқанын тексеруге, кемшіліктер мен ескертулерді тіркейтін қарау актісін жасауға және оларды жою мерзімін белгілеуге;",
    86: "6.2.2. Осы Шартта көзделген өзге құқықтарды, оның ішінде көзделген жағдайларда Шартты мерзімінен бұрын бұзу, Жалға алушыдан Үй-жайды қабылдау-тапсыру актісіне қол қоюды талап ету, Жалға алушы міндеттемелерін бұзған кезде Шарттың 7-бөліміндегі санкцияларды қолдану және жаңа мерзімге жаңа шарт жасасудан бас тарту құқықтарын жүзеге асыруға.",
    88: "7-БӨЛІМ. ТАРАПТАРДЫҢ ЖАУАПКЕРШІЛІГІ",
    89: "7.1. Жалға алушы Үй-жайдағы өрт және электр қауіпсіздігі ережелерінің сақталуына, техникалық құралдар мен инженерлік жабдықтың дұрыс пайдаланылуына және осы талаптарды тиісінше орындамаудың салдарына толық жауапты. Жалға алушы қандай да бір жұмысты орындау үшін өзі тартқан немесе Ғимараттың инженерлік желілеріне кіргізген барлық тұлғаларға, оның ішінде қызметкерлеріне, келушілеріне, мердігерлеріне және өзге контрагенттеріне жауапты.",
    90: "7.2. Жалдау ақысы және/немесе коммуналдық қызметтердің құны кешіктіріліп төленген жағдайда, Жалға алушы Жалға берушінің талабы бойынша мерзімі өткен соманың әрбір кешіктірілген күні үшін 0,5% мөлшерінде өсімпұл төлейді.",
    91: "7.3. Жалға беруші Үй-жайда немесе автотұрақта орналасқан Жалға алушының кез келген мүлкін ұрлау немесе бүлдіру салдарынан келтірілген залал немесе зиян үшін, сондай-ақ ондағы құндылықтардың, жеке және өзге мүліктің сақталуы үшін Жалға алушы алдында жауап бермейді.",
    92: "7.4. Жалға беруші Үй-жайда сақталатын Жалға алушының мүлкі және өзге тауарлық-материалдық құндылықтары үшін жауап бермейді; оларды сақтау шараларын Жалға алушы өз бетінше қабылдайды.",
    93: "7.5. Жалға беруші үшінші тұлғалардың әрекеттері салдарынан Үй-жайдың авариялық күйге келуі, коммуникациялардың ажыратылуы немесе Жалға алушы жабдығының не өзге мүлкінің істен шығуы үшін жауап бермейді.",
    94: "7.6. Жалға алушы жалдау ақысын немесе Шартта көзделген өзге төлемдерді 30 (отыз) күнтізбелік күннен артық кешіктірген жағдайда, Жалға беруші алдын ала жазбаша хабарлама жібергеннен кейін Үй-жайды электр энергиясынан ажыратуға және Жалға алушының өкілдері мен қызметкерлерін Үй-жайға кіргізбеуге (қол жеткізуді шектеуге) құқылы.",
    95: "Осы тармақта көрсетілген әрекеттер салдарынан Жалға алушыға келтірілуі мүмкін залал мен шығындар үшін Жалға беруші жауап бермейді.",
    96: "7.7. Шарт тоқтатылғаннан кейін Жалға алушы Үй-жайды уақтылы босатпаған жағдайда, ол Жалға берушіге мыналарды төлеуге міндетті:",
    97: "7.7.1. Үй-жайды қайтару мерзімін кешіктірген бүкіл кезең үшін оны пайдаланудың, пайдалану шығыстарының және коммуналдық қызметтердің құнын;",
    98: "7.7.2. Үй-жайды беру кешіктірілген әрбір күн үшін бір тоқсандық жалдау ақысының 1% мөлшерінде өсімпұл және Үй-жайды қайтаруды кешіктіруге байланысты Жалға берушінің залалдарын өтеу.",
    99: "7.8. Жалға алушы Қазақстан Республикасының уәкілетті органдары берген, Үй-жайда жүзеге асырылатын қызметке қажетті барлық лицензиялары мен өзге рұқсаттары бар екенін растайды және кепілдік береді. Егер лицензия немесе рұқсат мерзімінің өтуіне, күшінің жойылуына, тоқтатыла тұруына, қайтарып алынуына немесе өзге себептерге байланысты Жалға алушыда болмаса, Жалға алушы қажетті лицензиясыз немесе рұқсатсыз қызметті жүзеге асырғаны және Үй-жайды пайдаланғаны үшін Қазақстан Республикасының заңнамасына сәйкес дербес жауап береді.",
    100: "7.9. Жалға алушы Шарт бойынша ақшалай міндеттемелерді, шығыстарды немесе залалды өтеуді кешіктірген жағдайда, ол Жалға берушіге мерзімі өткен соманың әрбір кешіктірілген күні үшін 0,5% мөлшерінде өсімпұл төлейді.",
    101: "7.10. Шарт кез келген негіз бойынша немесе кез келген Тараптың бастамасымен тоқтатылған не бұзылған жағдайда, Жалға беруші қызмет басталғанға дейін жүргізілген Үй-жайдың күрделі жөндеуіне (әрлеу жұмыстарына) Жалға алушы жұмсаған шығындарды қайтармайды.",
    102: "7.11. Жалға алушы осы Шарт бойынша қабылдаған міндеттемелерінің орындалуы өз мүлкін ұстап қалу арқылы қамтамасыз етілуі мүмкін екеніне келіседі.",
    103: "7.12. Жалдау мерзімі аяқталғаннан кейін Жалға алушы мерзімінде алып кетпеген кез келген мүлікті Жалға беруші өз қалауы бойынша кез келген қолайлы тәсілмен шығара алады және/немесе басқа тұлғаларға сақтауға бере алады немесе қараусыз қалдыра алады; бұл ретте мүліктің сақталуы мен оны сақтау шығындары үшін жауап бермейді. Мүлікті шығару бойынша нақты шығыстардың өтелуін қамтамасыз ету үшін Жалға беруші мүліктің бір бөлігін өзінде қалдыра алады. Егер Жалға алушы 3 (үш) ай ішінде шығару шығындарын өтемесе, Жалға беруші талаптарын, оның ішінде Шарт бойынша өзге берешекті өтеу үшін мүлікті сатуға немесе оған өзгеше билік етуге құқылы. Осы жағдайларда Жалға алушы шығыстардың және сатылған мүлік құнының мөлшерлес еместігі туралы талап қоюға құқылы емес.",
    104: "7.13. Осы Шартта көзделген тұрақсыздық айыбын (айыппұлды, өсімпұлды) төлеу Тараптарды қабылдаған міндеттемелерін тиісінше орындаудан босатпайды.",
    105: "7.14. Жалға алушы азаматтың денсаулығына келтірілген зиянға (қар мен мұздан тазартылмаған баспалдақтан құлау, жарықтандырылмаған баспалдақ, еденді тиісті түрде дымқыл тазаламау немесе еденде қоқыстың болуы және басқа жағдайлар салдарынан болған жарақаттарға), сондай-ақ Үй-жайды қауіпсіз пайдалануды қамтамасыз етпеу немесе жазатайым оқиғалардың алдын алу үшін жеткілікті шараларды адал қабылдамау салдарынан келген мүліктік зиянға жауапты.",
    106: "7.15. Жалға алушы өзінің кінәсінен авариялық жағдайлар туындауы нәтижесінде Жалға берушіге және/немесе үшінші тұлғаларға келтірілген залал үшін жауапты.",
    107: "8-БӨЛІМ. ЕҢСЕРІЛМЕЙТІН КҮШ ЖАҒДАЙЛАРЫ",
    108: "8.1. Егер Шарт бойынша міндеттемелерді орындау табиғи апаттар, соғыстар, қарулы қақтығыстар, жаппай азаматтық тәртіпсіздіктер, эпидемиялар, табиғи немесе техногендік сипаттағы төтенше жағдайлар сияқты еңсерілмейтін күш мән-жайларының (бұдан әрі — Мән-жайлар) салдарынан мүмкін болмаса және олар Тараптардың Шарт бойынша міндеттемелерін орындауына тікелей әсер етсе, Тараптар міндеттемелерді орындамағаны немесе тиісінше орындамағаны үшін жауапкершіліктен босатылады.",
    109: "8.2. Еңсерілмейтін күш әсеріне ұшыраған Тарап Мән-жайлардың басталғаны және/немесе тоқтағаны туралы, олардың Шарт бойынша міндеттемелерді тиісінше орындауға әсер ету дәрежесін көрсете отырып, басталған немесе тоқтаған күннен бастап 10 (он) күннен кешіктірмей екінші Тарапқа жазбаша хабарлайды. Мән-жайлар кезеңінде Шарт толық немесе ішінара тоқтатыла тұруы мүмкін. Егер Мән-жайлар 60 (алпыс) күнтізбелік күннен артық жалғасып, тоқтау белгілері болмаса, Тараптар одан арғы әрекеттерді бірлесіп айқындайды және Шартты тоқтата тұруы немесе бұзуы мүмкін.",
    110: "8.3. Еңсерілмейтін күш мән-жайлары және олардың Шартты орындауға әсері туралы екінші Тарапты уақтылы жазбаша хабардар етпеген Тарап міндеттемелерді бұзғаны үшін жауапкершіліктен босатылу негізі ретінде осы мән-жайларға сілтеме жасау құқығынан айырылады.",
    112: "9-БӨЛІМ. ҚОРЫТЫНДЫ ЕРЕЖЕЛЕР",
    113: "9.1. Тараптар осы Шарттан туындайтын немесе оған байланысты кез келген даулар мен келіспеушіліктерді соттан тыс тәртіппен келіссөздер арқылы тату жолмен шешу үшін бар күшін салады. Бұлай реттеу мүмкін болмаған жағдайда даулар сот тәртібімен шешіледі. Тараптар шарттық соттылықты — Астана қаласының соттарын белгіледі.",
    114: "9.2. Осы Шартқа енгізілетін өзгерістер мен толықтырулар жазбаша түрде жасалып, Тараптардың уәкілетті өкілдері қол қойған және Тараптардың мөрлерімен расталған жағдайда ғана жарамды деп есептеледі.",
    115: "Тараптар екінші Тараптың жазбаша келісімінсіз осы Шарт бойынша өз құқықтары мен міндеттерін үшінші тұлғаларға беруге құқылы емес.",
    116: "9.4. Қазақстан Республикасының қолданыстағы заңнамасының талабы бойынша осы Шарттың қандай да бір бабының немесе ережесінің жарамсыз болуы Шарттың тұтастай жарамсыздығына әкеп соқпайды. Бұл жағдайда осы Шарттың қалған баптары мен ережелері Қазақстан Республикасының қолданыстағы заңнамасына қайшы келмейтін бөлігінде қолданылады.",
    117: "9.5. Осы Шарт қол қойылған күннен бастап күшіне енеді және Тараптар өздеріне қабылдаған міндеттемелерді толық орындағанға дейін қолданылады.",
    118: "9.6. Осы Шарт заңдық күші бірдей 2 (екі) түпнұсқа данада жасалып, қол қойылды, әр Тарапқа бір данадан беріледі.",
    120: "10-БӨЛІМ. ТАРАПТАРДЫҢ ДЕРЕКТЕМЕЛЕРІ, ҚОЛДАРЫ ЖӘНЕ МӨРЛЕРІ",
    122: "«_______________» ЖК,",
    123: "{{landlord_representative_name}} тұлғасында,",
    124: "ЖСН ____________",
    125: "Мекенжайы: ___________________",
    126: "ЖСК: _____________",
    127: "БСК: _______________",
    128: "Телефон нөмірі: ___________",
    131: "«_______________» ЖК,",
    132: "{{tenant_representative_name}} тұлғасында,",
    133: "ЖСН ____________",
    134: "Мекенжайы: ___________________",
    135: "ЖСК: _____________",
    136: "БСК: _______________",
    137: "Телефон нөмірі: ___________",
    142: "Жалға беруші                         Жалға алушы",
    144: "ЖК {{landlord_representative_name}}/қолы/             ЖК {{tenant_representative_name}}/қолы/",
}


FIELD_KEYS_BY_PARAGRAPH = {
    0: ["contract_number"],
    3: ["contract_day", "contract_month", "contract_year", "contract_city"],
    5: ["landlord_business_name", "landlord_representative_name", "landlord_iin", "landlord_address", "landlord_notice_number", "landlord_notice_date", "tenant_business_name", "tenant_iin", "tenant_address", "tenant_representative_name"],
    8: ["property_area", "property_area_words", "property_address"],
    12: ["property_use"],
    24: ["rent_until_date", "rent_amount_first", "rent_from_date", "rent_amount_second"],
    25: ["rent_charge_start_date", "actual_occupancy_date", "rent_free_start_date", "rent_free_end_date"],
    122: ["landlord_business_name"],
    123: ["landlord_representative_name"],
    124: ["landlord_iin"],
    125: ["landlord_address"],
    126: ["landlord_account"],
    127: ["landlord_bic"],
    128: ["landlord_phone"],
    129: [],
    131: ["tenant_business_name"],
    132: ["tenant_representative_name"],
    133: ["tenant_iin"],
    134: ["tenant_address"],
    135: ["tenant_account"],
    136: ["tenant_bic"],
    137: ["tenant_phone"],
    138: [],
    144: ["landlord_representative_name", "tenant_representative_name"],
}


FIELD_FALLBACKS = {
    "contract_number": "________",
    "contract_day": "____",
    "contract_month": "______________",
    "contract_year": "20___",
    "contract_city": "__________",
}


def _full_name(data):
    return " ".join(
        str(data.get(key, "")).strip()
        for key in ("surname", "last_name", "first_name", "patronymic")
        if str(data.get(key, "")).strip()
    )


def _normalised_data(data):
    values = dict(data)
    tenant_name = _full_name(data)
    if tenant_name:
        if not values.get("tenant_business_name"):
            values["tenant_business_name"] = tenant_name
        if not values.get("tenant_representative_name"):
            values["tenant_representative_name"] = tenant_name
    if not values.get("tenant_iin") and values.get("iin"):
        values["tenant_iin"] = values["iin"]
    if not values.get("rent_amount_first") and values.get("rent_amount"):
        values["rent_amount_first"] = values["rent_amount"]
    if not values.get("rent_amount_second") and values.get("rent_amount"):
        values["rent_amount_second"] = values["rent_amount"]
    return values


def _load_source_paragraphs():
    try:
        from docx import Document
    except ImportError as error:
        raise RuntimeError("Установите зависимости командой: python -m pip install -r requirements.txt") from error
    if not SOURCE_DOCX.exists():
        raise RuntimeError(f"Не найден шаблон договора: {SOURCE_DOCX}")
    return [paragraph.text for paragraph in Document(SOURCE_DOCX).paragraphs]


def _fill_blanks(paragraph, keys, values):
    position = 0

    def replace(match):
        nonlocal position
        key = keys[position] if position < len(keys) else None
        position += 1
        value = str(values.get(key, "")).strip() if key else ""
        raw = match.group(0)
        blank = value or "_" * len(re.search(r"_{2,}", raw).group(0))
        has_left_space = raw[:1] in {" ", "\t"}
        previous_is_digit = match.start() > 0 and paragraph[match.start() - 1].isdigit()
        left_space = " " if has_left_space or not previous_is_digit else ""
        return f"{left_space}{blank} "

    return re.sub(r"[ \t]*_{2,}[ \t]*", replace, paragraph)


def _additional_terms(values, language):
    labels = {
        "ru": {
            "heading": "Дополнительные сведения, заполненные в форме:",
            "lease_start_date": "Начало срока аренды",
            "lease_end_date": "Окончание срока аренды",
            "deposit_amount": "Залог",
            "payment_day": "День оплаты",
        },
        "en": {
            "heading": "Additional details entered in the form:",
            "lease_start_date": "Lease start date",
            "lease_end_date": "Lease end date",
            "deposit_amount": "Security deposit",
            "payment_day": "Payment day",
        },
        "kk": {
            "heading": "Нысанда толтырылған қосымша мәліметтер:",
            "lease_start_date": "Жалдау мерзімінің басталуы",
            "lease_end_date": "Жалдау мерзімінің аяқталуы",
            "deposit_amount": "Кепілдік жарна",
            "payment_day": "Төлем күні",
        },
    }[language]
    extras = [(key, str(values.get(key, "")).strip()) for key in ("lease_start_date", "lease_end_date", "deposit_amount", "payment_day")]
    extras = [(key, value) for key, value in extras if value]
    if not extras:
        return []
    return [labels["heading"]] + [f"{labels[key]}: {value}" for key, value in extras]


def build_contract_paragraphs(language="ru", data=None):
    data = _normalised_data(data or {})
    paragraphs = _load_source_paragraphs()
    translations = {"ru": {}, "en": PARAGRAPHS_EN, "kk": PARAGRAPHS_KK}.get(language, {})
    rendered = []
    for index, source in enumerate(paragraphs):
        paragraph = translations.get(index, source)
        if index == 142 and language == "ru":
            paragraph = paragraph.replace(
                "\t" * 5 + "   Арендатор",
                "\t" * 6 + " " * 84 + "Арендатор",
            )
        if index == 12:
            if language == "ru":
                paragraph = paragraph.replace("оказание косметологических услуг", "____________________________")
            else:
                paragraph = paragraph.replace("{{property_use}}", "____________________________")
        blank_keys = FIELD_KEYS_BY_PARAGRAPH.get(index, [])
        if index == 5 and language != "ru":
            blank_keys = [key for key in blank_keys if key not in {"landlord_representative_name", "tenant_representative_name"}]
        paragraph = _fill_blanks(paragraph, blank_keys, data)
        if index == 144 and language == "ru":
            paragraph = paragraph.replace(
                "\t\t             ", "\t\t" + " " * 38, 1
            )
        paragraph = paragraph.replace("{{landlord_representative_name}}", str(data.get("landlord_representative_name") or "__________"))
        paragraph = paragraph.replace("{{tenant_representative_name}}", str(data.get("tenant_representative_name") or _full_name(data) or "__________"))
        rendered.append(paragraph)

        if index == 128:
            rendered.append(_document_number_line(data, "landlord", language))
        elif index == 137:
            rendered.append(_document_number_line(data, "tenant", language))

    extras = _additional_terms(data, language if language in {"ru", "en", "kk"} else "ru")
    if extras:
        insert_at = next((i for i, line in enumerate(rendered) if "SECTION 10." in line or "10-БӨЛІМ" in line or "РАЗДЕЛ 10." in line), len(rendered))
        rendered[insert_at:insert_at] = [""] + extras + [""]
    return rendered


def build_contract_text(language="ru", data=None):
    return "\n".join(build_contract_paragraphs(language, data))


def _document_number_line(data, party, language):
    labels = {
        "ru": {"landlord": "Номер документа арендодателя", "tenant": "Номер документа арендатора"},
        "en": {"landlord": "Lessor ID document number", "tenant": "Lessee ID document number"},
        "kk": {"landlord": "Жалға берушінің жеке басын куәландыратын құжат нөмірі", "tenant": "Жалға алушының жеке басын куәландыратын құжат нөмірі"},
    }
    value = str(data.get(f"{party}_document_number", "")).strip()
    if party == "tenant" and not value:
        value = str(data.get("document_number", "")).strip()
    return f"{labels.get(language, labels['ru'])[party]}: {value or '____________'}"
