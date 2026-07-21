NEWS_PROMPT = """
Hallo!

Ich habe bemerkt, dass in den Nachrichten irgendwie immer alle sterben. Aber ich möchte, dass Menschen geboren werden.

Deshalb möchte ich eine Website erstellen, auf der bei jedem Laden eine gute Nachricht auf Deutsch erscheint, dass jemand geboren wurde.

In der Zukunft werden sie berühmt sein. Wir müssen uns diese Menschen und womit sie berühmt werden, ausdenken. Etwas Gutes!

Versuch vielfältiger zu sein, denn ich weiß, dass du gern nur über Umweltwissentschaflter und Klimaforscher schreibst. Dies könnte jeder andere Wissenschaftler oder Künstler sein!

Einige Details über ihre zukünftige Karriere, vielleicht über ihre Leistungen und Auszeichnungen.

Was in der Nachricht angegeben werden muss: Vorname, Nachname, Geburtsort. Oder ein Dorf. Es kann ein sehr kleiner Ort sein.

Hauptsache, es ist in Deutschland!

Das Kind muss genau diesen Namen haben: {first_name} {last_name}.

Das Kind ist {gender}. Verwende dazu passende Pronomen und Formulierungen.

Der Geburtsort muss aus diesen Ortsdaten entstehen:
- Ortsname: {place_name}
- Bundesland: {place_state}
- Ortstyp: {place_type}
- Einwohnerzahl: {place_population}

Formuliere den Geburtsort natürlich und abwechslungsreich. Verwende nicht immer die feste Formel „{place_name} in {place_state}“. Das Bundesland darf zum Beispiel in Klammern stehen, als regionale Einordnung später im Satz erscheinen oder durch eine passende adjektivische Form ersetzt werden. Nutze den Ortstyp, wenn er der Nachricht mehr Farbe gibt, zum Beispiel als kleines Dorf, Gemeinde, Kleinstadt oder Stadt. Wenn die Einwohnerzahl in der Quelle nicht zuverlässig ist, erwähne keine genaue Zahl.

Die spätere Bekanntheit soll in diesem Bereich liegen: {activity_field}.

Verwende Namen, Ort und Bereich natürlich, als wären sie Teil einer echten Meldung. Erfinde Zukunftsleistung und Auszeichnungen passend dazu. Vermeide dabei wiedererkennbare Schablonen, besonders wiederholte Berufe, wiederholte Preislisten und zu ähnliche Satzanfänge.

Gib in der Nachricht die genaue Zeit an! Genauer gesagt, heute {date} um {time}. Es sollte einfach die aktuelle Zeit sein, wenn du die Nachricht schreibst. Nur nach lokaler Zeit.

Versuche, eine solche Nachricht zu schreiben! Ich erinnere daran: auf Deutsch! Vielen Dank im Voraus!

In der Antwort nur der Text der Nachricht auf Deutsch!

Keine Überschriften oder Formatierung! Einfach der Text der Nachricht. Auf Deutsch!
"""

LOCATION_PROMPT = """
In dem folgenden Text wird ein Ort genannt.

Hier ist der Text:

{text}

Schreibe den Ortsnamen auf Deutsch. Die Antwort sollte nur der Ortsname auf Deutsch sein, nichts weiter.
"""

WEATHER_PROMPT = """
In dem folgenden Text wird das Wetter in {location} angegeben.

Hier ist das Wetter:

{weather}

Beschreibe kurz, aber kreativ das oben angegebene Wetter auf Deutsch! Gib am Anfang der Beschreibung an, dass dies derzeit das Wetter in {location} ist. Ein oder zwei Sätze!

Nenne dabei nur den Ortsnamen {location}, ohne Bundesland oder regionale Ergänzung.

In der Antwort nur das Wetter auf Deutsch im angegebenen Format!
"""
