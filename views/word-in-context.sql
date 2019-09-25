-- TODO: Look into limiting recursion
-- TODO: Add source name
WITH RECURSIVE WordInContext(ParentTextID, ChildTextID, ChildWordID, reading, SourceID, SourceName, begin, end, contents) AS (
    SELECT NULL, InitialText.id, NULL, "", InitialSource.id, InitialSource.name, 0, 0, InitialText.contents
    FROM orihime_text AS InitialText
    LEFT JOIN orihime_source AS InitialSource ON InitialSource.id = InitialText.source_id
    WHERE InitialText.id = %s
    UNION ALL
    SELECT ParentText.id,
           ChildText.id,
           ChildWord.id,
           ChildWord.reading,
           Source.id,
           Source.name,
           Relation.begin,
           Relation.end,
           ChildText.contents
    FROM WordInContext AS ParentWIC
    INNER JOIN orihime_text         AS ParentText ON ParentText.id    = ParentWIC.ChildTextID
    INNER JOIN orihime_word         AS ChildWord  ON ChildWord.id     = Relation.word_id
    INNER JOIN orihime_text         AS ChildText  ON ChildText.id     = ChildWord.definition_id
    LEFT  JOIN orihime_source       AS Source     ON Source.id        = ChildText.source_id
    INNER JOIN orihime_wordrelation AS Relation   ON Relation.text_id = ParentWIC.ChildTextID
  )
SELECT * from WordInContext;
