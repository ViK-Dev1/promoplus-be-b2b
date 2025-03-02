# AuthS

## Authentication Service

Microservizio dedicato per la registrazione e per l'autenticazione. Nello specifico al suo interno vengono gestite: la registrazione, l'autenticazione (login), cambio password e l'attivazione / disattivazione delle utenze.
<br>
### Istruzioni per l'utilizzo
- Se necessaria, la pwd del DB è nella cartella DB
- Per avviare questo servizio:
	1. Posizionarsi dal terminale nella cartella AuthS\Code (deve essere disponibile il main.py)
	1. Startare il server per le api <br> uvicorn main:app --reload --host 0.0.0.0 --port 8001
	1. Per debuggare:  <br> Andare sul debugger ed eseguire sul main.py così ogni breakpoint potrà essere provato e controllato
- Per disabilitare la documentazione per API di questo servizio basta indicare un url per la documentazione oppure impostarlo a None per disabilitarlo.
<br>
### Specifiche dettagliate
1. <b><u>Registrazione</u></b><br>
  Questo applicativo verrà utilizzato solo dai partner e dal loro staff. Per tale motivo la loro registrazione non si potrà fare in autonomia, ma verrà effettuata da utenti amministratori autorizzati. Sulla base di un elenco di utenti da registrare, verrà creata un'utenza per ciascuno di essi (se non è già presente).
1. <b><u>Autenticazione</u></b><br>
	Ciascun utente registrato può effettuare l'operazione di login indicando email / username e password. Per questioni di sicurezza, ad ogni accesso verrà inviata un'e-mail per indicare dell'accesso avvenuto e non sarà possibile accedere da più dispositivi contemporaneamente. Nel caso di tentativi di accesso sbagliati, la mail verrà inviata dopo il 5° e ultimo tentativo.
	<br><b>Attenzione: </b>Nel caso di utenze di amministratore e utenze di direzione del partner, l'operazione di login potrà avvenire in qualsiasi momento. Per quanto riguarda le utenze del gruppo staff, potranno essere vincolate a specifici orari e giornate per poter accedere al sistema.
	<br>Riassumendo:
	- Esito OK -> viene restituito un token jwt con cui l'utente potrà usare per usare le varie funzionalità utilizzabili solo da utenti registrati;
	- Esito KO -> se l'utente sbaglia più di 5 volte l'accesso, la sua utenza viene disattivata. Per poterla riattivare sarà necessario reimpostare la password o inviare richiesta esplicita via mail alla mail degli amministratori.
1. <b><u> Cambio password</u></b><br>
	Quest'operazione potrà essere richiesta dalla pagina dei dati personali dell'utente loggato oppure anche senza dover effettuare la login, ma indicando la casella postale associata alla propria utenza. Dunque verrà inviata un'e-mail con un link valido per 1 giorno. Se il link dovesse risultare ancora valido, allora si potrà procedere alla modifica effettiva, altrimenti si potrà richiedere un re-invio. Al completamento dell'operazione di modificasi riceverà un'e-mail di conferma.
1. <b><u>Attivazione</u></b><br>
	In seguito all'operazione di modifica password, se la propria utenza era stata disattivata a causa dei troppi tentativi sbagliati, allora ritornerà di nuovo attiva.<br>
	<b>Attenzione: </b>Se la disattivazione dell'utenza è stata effettuata manualmente da un'utente amministratore autorizzato oppure da un'utenza del gruppo di direzione del partner, la riattivazione potrà avvenire solo manualmente.
1. <b><u>Disattivazione</u></b><br>
	La disattivazione può avvernire in 2 modi differenti:
	1. In seguito al 5° tentativo sbagliato di autenticazione
	1. Immediatamente dopo l'operazione di eliminazione dell'utenza
	1. Un utenza di direzione del partner o un'amministratore autorizzato può disattivare le utenze che può gestire:
		- immediatamente e manualmente.
		- impostando delle regole in base all'orario di lavoro della persona associata all'utenza da gestire
		- impostando dei giorni / periodi specifici (ad esempio quando ci sono periodi festivi in cui l'attività del partner)

<br><i>Esempio</i><br>
Una persona potrebbe essere autorizzata ad entrare:
- in un orario specifico: (8-12;12:30-18:00) o all (qualsiasi orario)
- giorni specifici: Lun;Gio;Sab;Dom o all (qualsiasi giorno)
<br><br>
### Funzioni

```{eval-rst}
.. automodule:: CommonFun
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:
```