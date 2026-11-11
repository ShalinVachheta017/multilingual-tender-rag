# Verify the mini questions

Open each PDF at the page, confirm the expected answer, then set `verified_by_user` to `true` in `evaluation/datasets/mini_questions.json`.

## m01 (single_fact, de)

**Question:** Bis wann ist der Bieter bei der Ausschreibung Gerüstbauarbeiten für eine Sanierung (20046645) an sein Angebot gebunden?

**Expected answer:** Die Bindefrist endet am 15.06.2023.

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046645\DTAD_20046645_Vergabeunterlagen_20230406\VHB_211_Aufforderung_zur_Abgabe_eines_Angebots.pdf`
- **Page:** 1
- **Text in the index:** ...olmirstedt i.A. der Verbandsgemeinde Elbe-Heide August-Bebel-Straße 25 39326 Wolmirstedt Deutschland Tel.: +49 39201-64785 Fax: +49 39201-64799 Firma Bindefrist endet am 15.06.2023 Aufforderung zur Abgabe eines Angebots (Vergabeverfahren gemäß Abschnitt 1 der VOB/A) Bezeichnung der Bauleistung: Maßnahmennummer 32-EH.2023-VOB.Schm Baumaßnahme Neubau Feuerwehrgerätehaus Nachtweide 39517 Burgstall Ne...

## m02 (english_over_german, en)

**Question:** Until which date is a bidder bound to their offer for tender 20046904 (Sanierung Umkleidegebäude)?

**Expected answer:** The binding period (Bindefrist) ends on 26.05.2023.

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046904\DTAD_20046904_Vergabeunterlagen_20230406\000 Aufforderung und Bedingungen.pdf`
- **Page:** 1
- **Text in the index:** ...rzeit 11:00 Uhr Eröffnungstermin Datum 27.04.2023 Uhrzeit 11:00 Uhr Ort / Büroadresse Rathaus Michaelstr. 50, Eingang 5, 41460 Neuss Raum Raum: 1.629 Bindefrist endet am 26.05.2023 Aufforderung zur Abgabe eines Angebots (Vergabeverfahren gemäß Abschnitt 1 der VOB/A) Bezeichnung der Bauleistung Maßnahmennummer Baumaßnahme 65-23-60 Sanierung Umkleidegebäude Jahnstadion Vergabenummer Leistung 1315442...

## m03 (scanned_page, de)

**Question:** Wie hoch ist die Sicherheit für Mängelansprüche bei der Beräumungsausschreibung zur Umsetzung des Digitalpaktes (20046989) und ab welcher Auftragssumme muss sie geleistet werden?

**Expected answer:** 3 Prozent der Auftragssumme (inkl. Umsatzsteuer, ohne Nachträge), wenn die Auftragssumme mindestens 250.000 Euro ohne Umsatzsteuer beträgt.

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046989\DTAD_20046989_Vergabeunterlagen_20230406\Vergabeunterlagen-Los-1--Beraeumung.pdf`
- **Page:** 9
- **Text in the index:** ...tz. Ergänzung zu Punkt 5 - Sicherheitsleistungen für Mängelansprüche: Soweit die Auftragssumme mindestens 250.000 Euro ohne Umsatzsteuer beträgt, ist Sicherheit für Mängelansprüche in Höhe von drei Prozent der Auftragssumme (inkl. Umsatzsteuer, ohne Nachträge) zu leisten (vgl. § 7 SächsVergabeG). Weiterhin ist die Baubeschreibung Punkt 1 bis 1.5 im Leistungsverzeichnis zwingend zu beachten. © AR V...

## m04 (single_fact, de)

**Question:** Nach welchem Zuschlagskriterium wird bei der Sanierung des Umkleidegebäudes in Neuss (20046904) gewertet?

**Expected answer:** Zuschlagskriterium ist der Preis (ermittelt aus der Wertungssumme des Angebots).

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046904\DTAD_20046904_Vergabeunterlagen_20230406\000 Aufforderung und Bedingungen.pdf`
- **Page:** 3
- **Text in the index:** ... 211 Aufforderung zur Abgabe eines Angebots Stand 12/2019 Seite 4 von 4 7 Angebotswertung Kriterien für die Wertung der Haupt- und ggf. Nebenangebote Zuschlagskriterium Preis Der Preis wird aus der Wertungssumme des Angebotes ermittelt. Die Wertungssummen werden ermittelt aus den nachgerechneten Angebotssummen, insbesondere unter Berücksichtigung von Nachlässen, Erstattungsbetrag aus der Lohngleit...

## m05 (metadata, de)

**Question:** Welche Vergabestelle schreibt die Sanierung der Kappen und anschließende Beschichtung in Oedheim aus?

**Expected answer:** Landratsamt Heilbronn - Straßen und Verkehr, Lerchenstr. 40, 74072 Heilbronn.

**Source:** cleaned_metadata.xlsx, DTAD-ID 20046891, Spalte Vergabestelle (komplett)

## m06 (metadata, en)

**Question:** Which authority issued the tender for steel construction works (Stahlbauarbeiten) in Bernitt?

**Expected answer:** Stadt Bützow, Am Markt 1, 18246 Bützow.

**Source:** cleaned_metadata.xlsx, DTAD-ID 20046908, Spalte Vergabestelle (komplett)

## m07 (metadata, de)

**Question:** In welcher Region liegt die Ausschreibung Gerüstbauarbeiten für eine Sanierung (20046645), und welche Verfahrensart wird verwendet?

**Expected answer:** Region 39517 Burgstall; Verfahrensart: Öffentliche Ausschreibung.

**Source:** cleaned_metadata.xlsx, DTAD-ID 20046645, Spalten Region und Verfahrensart

## m08 (multi_document, de)

**Question:** Welche der beiden Ausschreibungen 20046645 (Gerüstbauarbeiten) und 20046904 (Umkleidegebäude) hat die spätere Bindefrist?

**Expected answer:** 20046645 (Bindefrist 15.06.2023) endet später als 20046904 (Bindefrist 26.05.2023).

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046645\DTAD_20046645_Vergabeunterlagen_20230406\VHB_211_Aufforderung_zur_Abgabe_eines_Angebots.pdf`
- **Page:** 1
- **Text in the index:** ...211 (Aufforderung zur Abgabe eines Angebots - Einheitliche Fassung) Datum der Versendung 05.04.2023 Vergabeart X Öffentliche Ausschreibung Beschränkte Ausschreibung ohne Teilnahmewettbewerb Beschränkte Ausschreibung mit Teilnahmewettbewerb Freihändig...

- **PDF:** `D:\Projects\multilingual-ragbot\data\extract_v1\20046904\DTAD_20046904_Vergabeunterlagen_20230406\000 Aufforderung und Bedingungen.pdf`
- **Page:** 1
- **Text in the index:** ...Stadt Neuss 211 Aufforderung zur Abgabe eines Angebots Stand 12/2019 Seite 1 von 4 Vergabestelle / Postadresse Gebäudemanagement Neuss Service GmbH c/o Stadtverwaltung Neuss Zentrale Vergabestelle Markt 2 41460 Neuss Tel. 02131 / 90 2531 Fax 02131 / ...

## m09 (unanswerable, de)

**Question:** Wer hat den Zuschlag für die Gerüstbauarbeiten (20046645) erhalten und mit welchem Angebotspreis?

**Expected answer:** Nicht in den Vergabeunterlagen enthalten (die Unterlagen enthalten keine Zuschlagsentscheidung).

**Source:** Die Vergabeunterlagen enthalten die Ausschreibung, nicht das Ergebnis. Bitte im PDF prüfen.

**Check:** search the tender's PDFs for an award decision (Zuschlag erteilt, Auftragnehmer). If none is stated, the expected answer is right.

## m10 (exact_id, en)

**Question:** What is the tender number DTAD-ID 20046904 about?

**Expected answer:** Sanierung Umkleidegebäude - Abbruch- und Rohbauarbeiten (Neuss, Augustinusviertel).

**Source:** cleaned_metadata.xlsx, DTAD-ID 20046904, Spalte Titel
