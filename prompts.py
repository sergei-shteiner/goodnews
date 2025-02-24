NEWS_PROMPT = """
Hallo!

Ich habe bemerkt, dass in den Nachrichten irgendwie immer alle sterben. Aber ich möchte, dass Menschen geboren werden.

Deshalb möchte ich eine Website erstellen, auf der bei jedem Laden eine gute Nachricht auf Deutsch erscheint, dass jemand geboren wurde.

In der Zukunft werden sie berühmt sein. Wir müssen uns diese Menschen und womit sie berühmt werden, ausdenken. Etwas Gutes!

Einige Details über ihre zukünftige Karriere, vielleicht über ihre Leistungen und Auszeichnungen.

Was in der Nachricht angegeben werden muss: Vorname, Nachname, Geburtsort. Oder ein Dorf. Es kann ein sehr kleiner Ort sein.

Hauptsache, es ist in Deutschland!

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

Schreibe es im Format "In {location} ist es gerade ...". Beschreibe dann kurz das oben angegebene Wetter auf Deutsch! Es müssen nicht genau diese Worte sein, solange es ein korrekter zusammenhängender Text ist.

In der Antwort nur das Wetter auf Deutsch im angegebenen Format!
"""
