
def match_studydesign_RCT(record):
    """ Identifies if a title/abstract is an RCT

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :return: 1 if title is identified as RCT, 2 if abstract is identified as an RCT, 0 if title and abstract do
                not have any RCT pattern. -1 if an error occurs when processing title, -2 if an error occurs when processing abstract
    """
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        pattern_title_rct = [[{"LOWER": {"IN": ['randomised', 'randomized']}}, {'IS_ASCII': True, 'OP': '*'}, {'LOWER': {"IN": ['trial', 'trials', 'study', 'studies']}}]]

        matcher.add("rct", pattern_title_rct)
        matches_title = matcher(doc_title, as_spans=True)
        matcher.remove("rct")
        if len(matches_title) > 0:
            #for span in matches_title:
            #    print(span.text, span.label_)
            return 1
        try:
            abstract = record['abstract']
            doc_abstract = nlp(abstract)
            pattern_abstract_rct = [[{'LOWER': {'REGEX': '^(random|parallel$|factorial$|crossover$)'}}],
                                    [{'LOWER': 'cross'}, {'LOWER': 'over'}],
                                    [{'LOWER': {'REGEX': '^(single|double|triple|quadruple)$'}}, {'LOWER':'blinded'}]]
            matcher.add("rct", pattern_abstract_rct)
            matches_abstract = matcher(doc_abstract, as_spans=True)
            if len(matches_abstract) > 0:
                matcher.remove("rct")
                pattern_abstract_rct = [[{"LOWER": 'results'}],
                                        [{'LOWER': {'REGEX': '^(outcome|significant)'}}]]
                matcher.add("rct", pattern_abstract_rct)
                matches_abstract = matcher(doc_abstract, as_spans=True)
                if len(matches_abstract) > 0:
                    return 2
                else:
                    return 0
        except Exception as e:
            return -2  # No abstract
        else:
            return 0
    except Exception as e:
        print(e)
        return -1


def match_studydesign_systematicrev(record):
    """ Identifies if a title is a systematic review/meta analysis

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :return: 1 if title is identified as a systematic review/meta analysis, 0 if title has no systematic review/meta analysis pattern.
            -1 if an error occurs when processing title
    """
    try:
      matcher = Matcher(nlp.vocab)
      title = record['title']
      doc_title = nlp(title)
      pattern_title_systematic = [[{'LOWER': {'REGEX': '^systematic'}}, {'IS_ASCII': True, 'OP': '?'},{'LOWER': {'REGEX': '^review'}}]]
      pattern_title_meta = [[{'LOWER': 'meta'}, {'LOWER': 'analysis'}]]
      matcher.add("sys", pattern_title_systematic)
      matcher.add("meta", pattern_title_meta)
      matches_title = matcher(doc_title, as_spans=True)
      if len(matches_title) > 0:
        return 1
      else:
        try:
          abstract = record['abstract']
          doc = nlp(abstract)
          matches_abstract = matcher(doc, as_spans=True)
          if len(matches_abstract) > 0:
            return 2
          else:
            return 0
        except Exception as e:
          return -2
    except Exception as e:
      print(e)
      return -1


def match_studydesign_observational(record):
    """ Identifies if a title/abstract is an observational study (cohort, case control, crosssectional)

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :return: 1 if title is identified as an observational study, 2 if abstract is identified as an observational study,
             0 if title and abstract do not have any observational study pattern.
             -1 if an error occurs when processing title, -2 if an error occurs when processing abstract
    """
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        pattern_title_obs = [[{'LOWER': 'case'}, {'LOWER': 'control'}],
                             [{'LOWER': 'cross'}, {'LOWER': 'sectional'}],
                             [{'LOWER': 'cohort'}]]
        matcher.add("obs", pattern_title_obs)
        matches_title = matcher(doc_title, as_spans=True)
        if len(matches_title) > 0:
            for span in matches_title:
                print(span.text, span.label_)
            return 1
        try:
            abstract = record['abstract']
            doc_abstract = nlp(abstract)
            matches_abstract = matcher(doc_abstract, as_spans=True)
            if len(matches_abstract) > 0:
                return 2
        except Exception as e:
            return -2  # No abstract
        else:
            return 0
    except Exception as e:
        print(e)
        return -1


def match_studydesign_other(record):
    """ Identifies if a title/abstract is a study of interest based on selected keywords

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :return: 1 if title is identified as an 'other' study, 2 if abstract is identified as an 'other' study,
             0 if title and abstract do not have any 'other' study pattern.
             -1 if an error occurs when processing title, -2 if an error occurs when processing abstract
    """
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        pattern_other = [[{'LOWER': {'REGEX': ('^(guideline|guidance|recommendations|algorithm|pathway)$')}}]]
        matcher.add("other", pattern_other)
        matches_title = matcher(doc_title, as_spans=True)
        if len(matches_title) > 0:
            for span in matches_title:
                print(span.text, span.label_)
            return 1
        try:
            abstract = record['abstract']
            doc_abstract = nlp(abstract)
            matches_abstract = matcher(doc_abstract, as_spans=True)
            if len(matches_abstract) > 0:
                return 2
        except Exception as e:
            return -2
        else:
            return 0
    except Exception as e:
        print(e)
        return -1


def match_relevant(record):
    """ Identifies if a title has no patterns which are considered irrelevant (eg. protocols, animal studies)

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :return: 0 if title is identified as an irrelevant study, 1 if no irrelevance detected
             -1 if an error occurs when processing title
    """
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        pattern_irrelevant = [
            [{'LOWER': {'REGEX': ('^(epidemiol|educat|training|assay|genetic|gene|protein|sequence|microbiol|'
                                  'mental|mice|comment|letter|editorial|income|africa|ppe|survey|school|porcine|pig|hamster|erratum|reply|response|'
                                  'school|dental|ophthalm|audiol|histopathol|tracheost|intub|protocol|correction|trace|'
                                  'sequen|enzyme|patho|mechanism|hypoth|theory|student|universit|infarction|personnel|workforce|nano|swab)')}}]]
        matcher.add("irrelevant", pattern_irrelevant)
        matches_title = matcher(doc_title, as_spans=True)
        if len(matches_title) > 0:
            return 0  # Not relevant
        else:
            return 1  # relevant to us
    except Exception as e:
        return -1


def match_longcovid(record, include_abstract):
    """ Identifies if the study is a 'long covid' study

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :param include_abstract: bool indicating whether to screen abstract for the pattern
    :return: 1 if 'long covid' pattern detected in the title, 2 if 'long covid' pattern detected in the abstract
             0 if no long covid pattern detected, -1 if an error occurred while processing title
             -2 if an error occurred while processing abstract (when include_abstract was TRUE)

    """
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        pattern_title = [[{"LOWER": {"REGEX": ('^(persist|protract|postdischarge$|postviral$|postcoronavirus$|postacute$|sequelae$|convalescent$|following$)')}}],
                         [{"LOWER": {"REGEX": ('^long+')}}, {"LOWER": {"REGEX": ('^(covid|term|lasting)$')}}],
                         [{"LOWER": 'post'}, {"LOWER": {"REGEX": ('^(covid|discharge|acute|sars|viral|critical)$')}}],
                         [{"LOWER": 'post'}, {"LOWER": {"REGEX": ('^(infect)')}}],
                         [{'LOWER': 'follow'}, {'LOWER': 'up'}],
                         [{'LOWER': 'months'}, {'LOWER': 'after'}],
                         [{'LOWER': {"REGEX": ('^(four|six|twelve)$')}}, {'LOWER': {"REGEX": ('^(month|months)$')}}],
                         [{'LIKE_NUM': True, 'OP': '+'}, {'LOWER':{"REGEX": ('^(month|months)$')}}]]
        
        matcher.add("longcovid", pattern_title)
        matches_title = matcher(doc_title)
        if (len(matches_title) > 0):
            return 1
        if include_abstract:
            try:
                abstract = record['abstract']
                doc_abstract = nlp(abstract)
                matches_abstract = matcher(doc_abstract, as_spans=True)
                if len(matches_abstract) > 0:
                    return 2
                else:
                    return 0
            except Exception as e:
                return -2  # No abstract
        else:
            return 0
    except Exception as e:
        print(e)
        return -1


def match_codeset(record, pattern, label, include_abstract):
    ''' Generic function to match patterns in title/abstract

    :param record: a row in the dataframe. The row will have a field 'title', and optionally 'abstract'
    :param pattern: Pattern to screen for
    :param label: label associated with this pattern
    :param include_abstract:Bool indicating whether to screen in the abstract in addition to title
                            1. title alone (include_abstract=0), 2. title or abstract (include_abstract = 1)
    :return: 1 if the pattern was found in the title, 2 if the pattern was found in the abstract
             0 if no pattern was found
             -1 if an error occurred while processing the title, -2 if an error occurred while processing the abstract
    '''
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        doc_title = nlp(title)
        matcher.add("label", pattern)
        matches_title = matcher(doc_title, as_spans=True)
        if len(matches_title) > 0:
            return 1
        if include_abstract:
            try:
                abstract = record['abstract']
                doc_abstract = nlp(abstract)
                matches_abstract = matcher(doc_abstract, as_spans=True)
                if len(matches_abstract) > 0:
                    return 2
                else:
                    return 0
            except Exception as e:
                return -2  # No abstract
        else:
            return 0
    except Exception as e:
        print(e)
        return -1



def match_management_codeset(record, include_abstract = 1):
    ''' Identify Management codeset (abstract is required)

    :param record: a row in the dataframe. The row will have a field 'title', and an 'abstract'
    :param include_abstract: Set this parameter to 1, the pattern for 'management' is screened in the abstract
    :return: 2 if pattern found in the abstract, 0 if no pattern is found.
             -1 if there was an error in the processing of the abstract
    '''
    try:
        matcher = Matcher(nlp.vocab)
        title = record['title']
        abstract = record['abstract']
        doc_abstract = nlp(abstract)
        pattern = [[{'LOWER': {'REGEX': ('^(symptom+)')}},
                    {'IS_ASCII': True, 'OP': '*'},
                    {'LOWER': {'REGEX': ('^(treat|improv|reduc)+')}}],
                   [{'LOWER': {'REGEX': ('^(treat|improv|reduc)+')}},
                    {'IS_ASCII': True, 'OP': '*'},
                    {'LOWER': {'REGEX': ('^(symptom+)')}}]]
        matcher.add("management", pattern)
        matches_abstract = matcher(doc_abstract, as_spans=True)
        if len(matches_abstract) > 0:
            exclusion_pattern = [[{'LOWER': {'REGEX': ('^(icu|severe)$')}}]]
            matcher.remove("management")
            matcher.add("management", exclusion_pattern)
            matches_abstract = matcher(doc_abstract, as_spans=True)
            if len(matches_abstract) > 0:
                return 0  # not interested if ICU/severe conditions
            else:
                return 2
    except Exception as e:
        print(e)
        return -1

    return 0

