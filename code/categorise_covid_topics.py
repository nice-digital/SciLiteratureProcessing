# Categories supported by this software
SUPPORTED_CATEGORIES = ['RCT', 'SYST-META', 'OBSERVATIONAL', 'RELEVANT',
                        'REMDESIVIR', 'TOCILIZUMAB', 'SARILUMAB', 'IVERMECTIN',
                        'ASPIRIN', 'BUDESONIDE', 'CORTICOSTEROIDS', 'ANTIBIOTICS',
                        'COLCHICINE', 'AZITHROMYCIN','LONG COVID', 'NAb', 'SACT', 'BONE MARROW',
                        'ASTHMA', 'RHEUMATOLOGY', 'COPD', 'CYSTIC FIBROSIS', 'PREGNANCY',
                        'MYOCARDIAL', 'GASTRO', 'KIDNEY', 'DERMATOLOGY', 'VIT C', 'VIT D',
                        'VIIT', 'VTE','RESPIRATORY', 'PLANNED CARE', 'INTERSTITIAL LUNG', 'CO_INFECTION',
                        'MANAGEMENT', 'ASSESSMENT','CYP IMMUNOSUPPRESSION', 'THERAPEUTICS'
                        ]


def categorise_topics_covid(data, topic_list=SUPPORTED_CATEGORIES):
    """ Identify the presence of requested categories/patterns in the title/abstract

    :param data: dataframe consisting of rows of studies (title and abstracts. Abstract is optional for all but one category)
    :param topic_list: Requested categories
    :return: original dataframe with extra columns. Each extra column represents a requested category.
             Values in that column indicates whether the study has a matching pattern for that category.
    """
    logging.info("RCT")
    data['RCT'] = data.apply(match_studydesign_RCT, axis=1)
    logging.info("Systematic Review/Meta-analysis")
    data['Syst-Meta'] = data.apply(match_studydesign_systematicrev, axis=1)

    if 'OBSERVATIONAL' in topic_list:
        logging.info("Observational")
        data['observational'] = data.apply(match_studydesign_observational, axis=1)
    #data['other-design'] = data.apply(match_studydesign_other, axis=1)

    if 'RELEVANT' in topic_list:
        logging.info("Subject Relevant")
        data['subject relevant'] = data.apply(match_relevant, axis=1)

    if 'REMDESIVIR' in topic_list:
        logging.info("Remdesivir")
        data['remdesivir'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'remdesivir'}]], "remdesivir", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'TOCILIZUMAB' in topic_list:
        logging.info("Tocilizumab")
        data['tocilizumab'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'tocilizumab'}]], "tocilizumab", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'SARILUMAB' in topic_list:
        logging.info("Sarilumab")
        data['sarilumab'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'sarilumab'}]], "sarilumab", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'IVERMECTIN' in topic_list:
        logging.info("Ivermectin")
        data['ivermectin'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'ivermectin'}]], "ivermectin", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'ASPIRIN' in topic_list:
        logging.info("Aspirin")
        data['aspirin'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'aspirin'}]], "aspirin", 0)), axis=1)

    if 'BUDESONIDE' in topic_list:
        logging.info("Budesonide")
        data['budesonide'] = data.apply(
            (lambda row: match_codeset(row, [[{'LOWER': 'budesonide'}]], "budesonide", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'CORTICOSTEROIDS' in topic_list:
        logging.info("Corticosteroids")
        pattern = [[{'LOWER': {'REGEX': (
            '^(corticosteroid|dexamethasone|hydrocortisone|fludrocortisone|glucocorticoid|steroid|prednisolone)')}}]]
        data['corticosteroids'] = data.apply(
            (lambda row: match_codeset(row, pattern, "corticosteroids", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'ANTIBIOTICS' in topic_list:
        logging.info("Antibiotics")
        pattern = [[{'LOWER': {'REGEX': ('^(azithromycin|doxycycline|antibiotic|antibacter|bactericid|antimicrob)')}}]]
        data['antibiotics'] = data.apply((lambda row: match_codeset(row, pattern, "antibiotics", (row['RCT'] or row['Syst-Meta']))),
                                                       axis=1)
    if 'COLCHICINE' in topic_list:
        logging.info("Colchicine")
        pattern = [[{'LOWER': {'REGEX': ('^(colchicine|colcrys|mitigare|gloperba)$')}}]]
        data['colchicine'] = data.apply((lambda row: match_codeset(row, pattern, "colchicine", (row['RCT'] or row['Syst-Meta']))),
                                                      axis=1)

    if 'LONG COVID' in topic_list:
        logging.info("Long Covid")
        data['longcovid'] = data.apply((lambda row: match_longcovid(row, 0)), axis=1)

    if 'NAb' in topic_list:
        logging.info("Neutralizing Antibodies")
        pattern = [[{'LOWER': {'REGEX': '^neutralizing$'}}, {'LOWER': {'REGEX': ('^antibod')}}],
                [{'LOWER': {'REGEX': '^neutralizing$'}}, {'LOWER': {'REGEX': '^monoclonal$'}}],
                [{'LOWER': {'REGEX': '^monoclonal$'}}, {'LOWER': {'REGEX': ('^antibod')}}],
                [{'LOWER': {'REGEX': '^(bamlanivimab|imdevimab|casirvimab|sotrovimab|etesvimab|regen|adalimumab)$'}}]]
        data['neutralizingantibody'] = data.apply(
                (lambda row: match_codeset(row, pattern, "neutralizingantibody", (row['RCT'] or row['Syst-Meta']))), axis=1)

    if 'SACT' in topic_list:
        logging.info("SACT")
        pattern = [[{'LOWER': {'REGEX': (
            '^(cancer|oncolog|chemo|chemotherap|radiotherap|carcinoma$|lymphoma$|malign|melanoma$|polyp|leukaemia|radiation$)')}}]]
        data['chemo'] = data.apply((lambda row: match_codeset(row, pattern, "chemo", 0)), axis=1)

    if 'BONE MARROW' in topic_list:
        logging.info("Bone marrow")
        pattern = [[{'LOWER': {'REGEX': ('^(hematopoietic|haematopoietic)$')}}]]
        data['bonemarrow'] = data.apply((lambda row: match_codeset(row, pattern, "bonemarrow", 0)),
                                                      axis=1)

    if 'ASTHMA' in topic_list:
        logging.info("Asthma")
        pattern = [[{'LOWER': {'REGEX': ('^asthma')}}]]
        data['asthma'] = data.apply((lambda row: match_codeset(row, pattern, "asthma", 0)), axis=1)

    if 'RHEUMATOLOGY' in topic_list:
        logging.info("Rheumatology")
        pattern = [[{'LOWER': {'REGEX': ('^rheumat|bdmards|tsdmards')}}]]
        data['rheumatology'] = data.apply((lambda row: match_codeset(row, pattern, "rheumatology", 0)),
                                                        axis=1)

    if 'COPD' in topic_list:
        logging.info("COPD")
        pattern = [[{'LOWER': {'REGEX': ('^copd$')}}]]
        data['copd'] = data.apply((lambda row: match_codeset(row, pattern, "copd", 0)), axis=1)

    if 'CYSTIC FIBROSIS' in topic_list:
        logging.info("Cystic Fibrosis")
        pattern = [[{"LOWER": "cystic"}, {"LOWER": "fibrosis"}]]
        data['cysticfibrosis'] = data.apply(
            (lambda row: match_codeset(row, pattern, "cysticfibrosis", 0)), axis=1)

    if 'PREGNANCY' in topic_list:
        logging.info("Pregnancy")
        pattern = [[{'LOWER': {'REGEX': ('^(pregnancy|pregnant|obstetric|abortion)$'
                                     '^(maternal|fetal|antenatal|postnatal|intrapartum|perinatal|breastfeed|breastfeeding)$')}}]]
        data['pregnancy'] = data.apply((lambda row: match_codeset(row, pattern, "pregnancy", 0)), axis=1)

    if 'MYOCARDIAL' in topic_list:
        logging.info("Myocardial")
        pattern = [[{'LOWER': {'REGEX': ('(^myocardial|cardiac)$')}}],
                [{'LOWER': 'coronary'}, {'LOWER': 'artery'}]]
        data['myocardial'] = data.apply((lambda row: match_codeset(row, pattern, "myocardial", 0)),
                                                      axis=1)

    if 'GASTRO' in topic_list:
        logging.info("Gastro")
        pattern = [[{'LOWER': {'REGEX': ('^(gastro|bowel$|gi$|ibd$|digest|endoscopy$|liver$)')}}]]
        data['gastro'] = data.apply((lambda row: match_codeset(row, pattern, "gastro", 0)), axis=1)

    if 'DERMATOLOGY' in topic_list:
        logging.info("Dermatology")
        pattern = [[{'LOWER': {'REGEX': ('^(psoriasis$|dermatolog|dermatitis|bullous$|cutaneous$|dermoscopy$|psoria)')}}],
                [{'LOWER': 'skin'}, {'LOWER': 'diseases'}]]
        data['dermatology'] = data.apply((lambda row: match_codeset(row, pattern, "dermatology", 1)),
                                                       axis=1)

    if 'KIDNEY' in topic_list:
        logging.info("Kidney")
        pattern = [[{'LOWER': {'REGEX': ('^(dialy|haemodialysis$|kidney$|renal|hemodialysis$|nephr|aki$|ckd$)')}}]]
        data['kidney'] = data.apply((lambda row: match_codeset(row, pattern, "kidney", 0)), axis=1)

    if 'VIT D' in topic_list:
        logging.info("Vitamin D")
        pattern = [[{'LOWER': {'REGEX': ('^(vitamin|vit|hydroxyvitamin|hypovitaminosis)$')}}, {'LOWER': {'IN': ['d', 'd3']}}],
                [{'LOWER': {'REGEX': ('^(cholecalciferol|ergocalciferol|calcifediol)$')}}]]
        data['vitaminD'] = data.apply((lambda row: match_codeset(row, pattern, "vitaminD", 1)), axis=1)

    if 'VIT C' in topic_list:
        logging.info("Vitamin C")
        pattern = [[{"LOWER": "vitamin"}, {"LOWER": "c"}],
                [{"LOWER": "ascorbic"}, {"LOWER": "acid"}]]
        data['vitaminC'] = data.apply((lambda row: match_codeset(row, pattern, "vitaminC", 0)), axis=1)

    if 'INTERSTITIAL LUNG' in topic_list:
        logging.info("Interstitial Lung")
        pattern = [[{"LOWER": "interstitial"}, {"LOWER": "lung"}],
                    [{'LOWER': 'ild'}]]
        data['interstitiallung'] = data.apply((lambda row: match_codeset(row, pattern, "lung", 1)),
                                                            axis=1)

    if 'VIIT' in topic_list:
        logging.info("VIIT")
        pattern = [[{'LOWER': {'REGEX': ('^vaccin')}}, {'IS_ASCII': True, 'OP': '*'}, {'LOWER': {'REGEX': ('^thrombo')}}],
                [{'LOWER': {'REGEX': ('^thrombo')}}, {'IS_ASCII': True, 'OP': '*'}, {'LOWER': {'REGEX': ('^vaccin')}}],
                [{'LOWER': {'REGEX': ('^(viit|tts|vipit)$')}}],
                [{'LOWER': 'thrombosis'}, {'LOWER': 'with'}, {'LOWER': 'thrombocytopenia'}, {'LOWER': 'syndrome'}],
                [{'LOWER': {'REGEX': ('^vaccin')}}, {'IS_ASCII': True, 'OP': '*'},
                    {'LOWER': {'REGEX': ('^prothrombo')}}]]
        data['viit'] = data.apply((lambda row: match_codeset(row, pattern, "viit", 1)), axis=1)

    if 'MANAGEMENT' in topic_list:
        logging.info("Management")
        data['management'] = data.apply((lambda row: match_management_codeset(row, 1)), axis=1)

    if 'RESPIRATORY' in topic_list:
        logging.info("Respiratory")
        pattern = [[{'LOWER': 'respiratory'}, {'IS_ASCII': True, 'OP': '*'},
                    {'LOWER': {'REGEX': ('^(failure|support|non-invasive|noninvasive|invasive|cpap|hfno|oxygen)$')}}],
                [{'LOWER': {'REGEX': ('^(failure|support|non-invasive|invasive|cpap|hfno|oxygen)$')}},
                    {'IS_ASCII': True, 'OP': '*'}, {'LOWER': 'respiratory'}]]
        data['resp'] = data.apply((lambda row: match_codeset(row, pattern, "resp", 0)), axis=1)

    if 'CO_INFECTION' in topic_list:
        logging.info("Co-Infection")
        pattern = [[{'LOWER': {'REGEX': ('^(coinfect)')}}],
                [{'LOWER': {'REGEX': ('^(co|secondary|cross|super)$')}}, {'LOWER': {'REGEX': ('^(infect)')}}],
                [{'LOWER': {'REGEX': ('^bacteria')}}, {'LOWER': {'REGEX': ('^infect')}}]]
        data['coinfection'] = data.apply((lambda row: match_codeset(row, pattern, "coinfection", 0)),
                                                       axis=1)

    if 'PLANNED CARE' in topic_list:
        logging.info("Planned Care")
        pattern = [[{'LOWER': {'REGEX': ('^(telemedicine|elective|service|delivery|clinic|surgery|admissions)$')}}]]
        data['plannedcare'] = data.apply((lambda row: match_codeset(row, pattern, "plannedcare", 0)),
                                                       axis=1)
    if 'VTE' in topic_list:
        logging.info("VTE")
        pattern = [[{'LOWER': {'REGEX': ('^(thrombo|anticoag|heparin|coag|procoag|hypercoag|antithrombo)')}}],
                [{'LOWER': 'pulmonary'}, {'LOWER': 'embolism'}]]
        data['vte'] = data.apply((lambda row: match_codeset(row, pattern, "vte", 0)), axis=1)

    if 'ASSESSMENT' in topic_list:
        logging.info("Assessment")
        pattern = [[{'LOWER': {'REGEX': ('^(symptom|sign)')}}, {'IS_ASCII': True, 'OP': '*'},
                    {'LOWER': {'REGEX': ('^(fever|temperature|cough|headache|smell|taste|anosmia|ageusia)')}}],
                [{'LOWER': {'REGEX': ('^(fever|temperature|cough|headache|smell|taste|anosmia|ageusia)')}},
                    {'IS_ASCII': True, 'OP': '*'}, {'LOWER': {'REGEX': ('^(symptom|sign)')}}]]
        data['assessment'] = data.apply((lambda row: match_codeset(row, pattern, "assessment", 1)),
                                                      axis=1)
    if 'AZITHROMYCIN' in topic_list:
        logging.info("Azithromycin")
        pattern = [[{'LOWER': 'azithromycin'}]]
        data['azithromycin'] = data.apply((lambda row: match_codeset(row, pattern, "azithromycin", 0)),
                                                        axis=1)
    if 'CYP IMMUNOSUPPRESSION' in topic_list:
        logging.info("CYP Immunosuppression")
        pattern = [[{'LOWER': {'REGEX': ('^(pediatric|infant|baby|child)')}}]]
        data['cypImmunosuppression'] = data.apply(
            (lambda row: match_codeset(row, pattern, "cypImmunosuppression", 0)), axis=1)

    # TODO: this pattern needs fine-tuning especially any words separated by hyphen should be processed differently
    if 'THERAPEUTICS' in topic_list:
        logging.info("Therapeutics")
        pattern = [[{'LOWER': {
            'REGEX': ('^(anakinra|azithromycin|colchicine|dexamethasone|favipiravir|hydrocortisone|hydroxychloroquine)'
                     '^(interferon|lopinavir|ritonavir|mesenchymal|methylprednisolone|prednisolone|remdesivir)'
                    '^(ruxolitinib|sarilumab|tocilizumab|ravulizumab|baricitinib|oseltamivir|dornase|anticoagulant|heparin|enoxaparin|sodium|sofosbuvir)'
                    '^(daclatasvir|interferon|canakinumab|ivermectin|ciclesonide|doxycycline|losartan|vitamin|melatonin|acetylcysteine|ciclosporin)'
                    '^(povidone|ibuprofen|naproxen|indometacin|indomethacin|celecoxib|celebrex|nimesulide|nimefen|zinc|bamlanivimab|ly3819253|ly|cov555)'
                    '^(casirivimab|imdevimab|regn10933|regn10987|regn|cov2|human|immunoglobulin|imatinib|molnupiravir|nitazoxanide|acalabrutinib)'
                     '^(calquence|emtricitabine|tenofovir|aspirin|rivaroxaban|camostat|mesylate|nafamostat|mesylate|otilimab|niclosamide|lenzilumab)'
                     '^(mavrilimumab|namilumab|tj003234|plonmarlimab|cd24fc|siltuximab|clazakizumab|cmab-806|tocilizumab|levilimab|olokizumab|sirukumab)'
                     '^(azd7442|azd8895|azd1061|tixagevimab|cilgavimab|ct-p59|regdanvimab|adalimumab|etanercept|infliximab|gimsilumab|budesonide|fluoxetine)'
                     '^(fluvoxamine|nintedanib|pirfenidone|pln-74809|in01|atr-002|pamrevlumab|td139|xc-268BG|vir-7831|sotrovimab|vir-7832|aviptadil|pemziviptadil)'
                     '^(statin+|atorvastatin|rosuvastatin|simvastatin|nitric|nitroglycerin|resp301|sodium|dapagliflozin|anti-platelets|clopidogrel|prasugrel)'
                     '^(ticagrelor|proxalutamide|enzalutamide|bicalutamide|leronlimab|maraviroc|cenicriviroc|sargramostim|molgramostim|montekulast)'
                     '^(brii-196|brii-198|dzif-10c/bic67551|bgb-dxp593|bgb-dxb604|sti-2020|covi-amg|sti-1499|covi-guard|scta01|ty-027|adg20|antiviral|at-527)'
                     '^(ribavirin|enisamium|iodide|galidesivir|pf-07321332|ace|ramipril|lisinopril|perindopril|enalapril|trandolapril|captopril|iota-carrageenan)'
                     '^(arb|valsartan|cadesartan|irbesartan|telmisartan|lmesartan|eprosartan|sacubitril|valsartan|trv-027|tofacitinib|dasatinib|fostamatinib|ensovibep)')}}],
                [{'LOWER': 'convalescent'}, {'LOWER': 'plasma'}]]
        data['therapeutics'] = data.apply((lambda row: match_codeset(row, pattern, "therapeutics", 0)),
                                                        axis=1)
    return data




