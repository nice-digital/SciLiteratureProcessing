
puncts = ['!', '[', ']', ',', '.', ':', ',', '{', '}', '/', '\\',
        '@', '#', '$', '%', '&', '_', '*', '~', "'", '-','?', '(', ')']

def remove_punctuation(field):
  """ Replaces punctuations with space

  :param field:text which has punctuations
  :return: text with punctuations replaced with spaces,
           or a null string in case of exception.
  """
  try:
    x = field
    for punct in puncts:
      if punct in x:
        x = x.replace(punct, f' ')
  except:
    return " "
  return x


def preproc_title(df):
  ''' Preprocess Title

  :param df: dataframe which has a field 'title'
  :return: dataframe where the 'title' field's contents are
          pre-processed (lower case, strip leading and trailing spaces, replace punctuations with space).
          Original title is copied into a new field called 'origTitle'
  '''
  if not df.empty:
    df['origTitle'] = df['title']
    df['title'] = df['title'].str.lower()
    df['title'] = df['title'].str.strip()
    df['title'] = df['title'].apply(remove_punctuation)
  return df

def preproc_abstract(df):
  ''' Preprocess Abstract

  :param df: dataframe which has a field 'abstract'
  :return: dataframe where the 'abstract' field's contents are
            pre-processed (lower case, strip leading and trailing spaces, replace punctuations with space).
            Original abstract is copied into a new field called 'origAbstract'
  '''
  if not df.empty:
    df['origAbstract'] = df['abstract']
    df['abstract'] = df['abstract'].str.lower()
    df['abstract'] = df['abstract'].str.strip()
    df['abstract'] = df['abstract'].apply(remove_punctuation)
  return df
