# UserS

## User Service
<b>DA COMPLETARE PER BENE QUANDO MI DEDICHERò A QUESTO SERVIZIO</b>
Microservizio dedicato per la 
- gestione degli utenti e dei gruppi a cui essi possono essere associati.
- registrazione di nuovi utenti
- l'attivazione / disattivazione delle utenze
<br>
### Istruzioni per l'utilizzo
ciao
<br>
### Specifiche dettagliate
1. <b><u>Registrazione</u></b><br> La registrazione è un'operazione ammessa solo per gli utenti amministratori
1. <b><u>Attivazione</u></b><br>
	Se la disattivazione dell'utenza è stata effettuata manualmente da un'utente amministratore autorizzato oppure da un'utenza del gruppo di direzione del partner, la riattivazione potrà avvenire solo manualmente.
1. <b><u>Disattivazione</u></b><br>
	La disattivazione può avvernire in 2 modi differenti:
	1. Immediatamente dopo l'operazione di eliminazione dell'utenza
	1. Un utenza di direzione del partner o un'amministratore autorizzato può disattivare le utenze che può gestire:
		- immediatamente e manualmente.
		- impostando delle regole in base all'orario di lavoro della persona associata all'utenza da gestire
		- impostando dei giorni / periodi specifici (ad esempio quando ci sono periodi festivi in cui l'attività del partner)
1. Eliminazione di un utente: PSEUDODENOMINIZZAZIONE (conforme al GDPR) questa operazione comporta l'oscuramento dei dati degli utenti cancellati, in modo da preservare le loro attività per analisi future, ma non rendendo più possibile risalire all'identità dell'utente reale. Deve portare a delle modifiche anche nella tabella del servizio AuthS
<br>
### Endpoints
<b>[P]</b> - endpoint pubblico
<br><b>[L]</b> - endpoint per utenti loggati
<br><b>[IC]</b> - endpoint per la comunicazione interna 
<br><b>[A]</b> - endpoint solo per admin<br><br>
- <span class='pre'>[A] | registerUsers</span><br>richiesta proveniente dal servizio UserS solamente da utenti di tipo amministratore - registra nuovi utenti<br>
- <span class='pre'>[IC] | reactivateUsers</span><br>richiesta proveniente dal servizio UserS - riattiva le utenze degli utenti indicati, sia dal punto di vista del campo userDisabledPwd che userDisabled<br>
- <span class='pre'>[IC] | disableUsers</span><br>richiesta proveniente dal servizio UserS - disattiva le utenze degli utenti indicati, agendo su userDisabled<br>
- <span class='pre'>[IC] | changeUsrData</span><br>richiesta proveniente dal servizio UserS - permette di cambiare username, email per un utente specifico<br>
- <span class='pre'>[IC] | changeUsrPwd</span><br>richiesta proveniente dal servizio UserS - permette di cambiare password per un utente specifico<br>
- <span class='pre'>[IC] | changeUsersUsabilityTD</span><br>richiesta proveniente dal servizio UserS - cambia time e days riferiti alla usability degli utenti indicati<br>