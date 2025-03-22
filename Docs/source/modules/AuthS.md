# AuthS

## Authentication Service

Microservizio dedicato per la registrazione e per l'autenticazione. Nello specifico al suo interno vengono gestite: la registrazione, l'autenticazione (login) e il cambio password.
<br>
### Istruzioni per l'utilizzo
- Se necessaria, la pwd del DB è nella cartella DB
- Per avviare questo servizio: 
	1. Posizionarsi con un terminale aperto in VisualStudio nella cartella AuthS\Code (deve essere disponibile il main.py)
	1. Attivare il virtualenv che include tutte le librerie necessarie per questo progetto <br>
		<b>Per attivarlo </b> ..\..\..\Configs\AuthS\venv-AuthS\Scripts\activate<br>
		<b>Per disattivarlo </b> deactivate
	1. Startare il server per le api <br> uvicorn main:app --reload --host 0.0.0.0 --port 8001
	1. Per debuggare:  <br> Andare sul debugger ed eseguire sul main.py così ogni breakpoint potrà essere provato e controllato
	1. <span class='pre'>TEST AUTOMATICI</span>: per eseguire test automatici già preparati, aprire un cmd, posizionarsi nella cartella Test ed eseguire  'pytest --html=report_test1.html' (ovviamente avendo già attivato: la virtual machine, il db e l'api del servizio) 
- Per disabilitare la documentazione per API di questo servizio basta indicare un url per la documentazione oppure impostarlo a None per disabilitarlo.
<br>
### Checklist delle schermate
1. VM
1. cmd (vs code)
	- ssh verso la VM
	- test : 'pytest --html=report_test1.html'
	- rebuild della documentazione : '.\make clean' e poi '.\make html'
	- debugger in python
1. VS code
	- service documentation page
1. Brave browser
	- documentazione
	- risultati testing
1. Insomnia
	- api testing
<br>
### Specifiche dettagliate
1. <b><u>Registrazione</u></b><br>
  Questo applicativo verrà utilizzato solo dai partner e dal loro staff. Per tale motivo la loro registrazione non si potrà fare in autonomia, ma verrà effettuata dagli utenti amministratori. Sulla base di un elenco di utenti da registrare, verrà creata un'utenza per ciascuno di essi (se non è già presente).
1. <b><u>Autenticazione</u></b><br>
	Ciascun utente registrato può effettuare l'operazione di login indicando email / username e password. Per questioni di sicurezza, ad ogni accesso verrà inviata un'e-mail per indicare dell'accesso avvenuto e non sarà possibile accedere da più dispositivi contemporaneamente. Nel caso di tentativi di accesso sbagliati, la mail verrà inviata dopo il 5° e ultimo tentativo.
	<br><b>Attenzione: </b>Le utenze di amministratore saranno le uniche ad avere come username USERNAME-admin.
	<br><b>Attenzione: </b>Le utenze dei partner avranno come username USERNAME-partner.
	<br><b>Attenzione: </b>Nel caso di utenze di amministratore e utenze di direzione del partner, l'operazione di login potrà avvenire in qualsiasi momento. Per quanto riguarda le utenze del gruppo staff, potranno essere vincolate a specifici orari e giornate per poter accedere al sistema.
	<br>Riassumendo:
	- Esito OK -> viene restituito un token jwt con cui l'utente potrà usare per usare le varie funzionalità utilizzabili solo da utenti registrati;
	- Esito KO -> se l'utente sbaglia più di 5 volte l'accesso, la sua utenza viene disattivata. Per poterla riattivare sarà necessario reimpostare la password o inviare richiesta esplicita via mail alla mail degli amministratori.
1. <b><u> Cambio password</u></b><br>
	Nel caso di utenze nuove, l'utente dovrà procedere alla modifica immediata, perchè la password associata all'utenza sarà corretta, ma scaduta.
	Quest'operazione potrà essere richiesta anche esplicitamente :
	- dalla pagina dei dati personali dell'utente loggato
	- senza dover effettuare la login, ma indicando la casella postale associata alla propria utenza.<br>
	Dunque verrà inviata un'e-mail con un link valido per 1 giorno. Se il link dovesse risultare ancora valido, allora si potrà procedere alla modifica effettiva, altrimenti si potrà richiedere un re-invio. Al completamento dell'operazione di modifica si riceverà un'e-mail di conferma e l'utenza verrà riattivata, nel caso si fosse disabilita per numerosi tentativi errati.
	

<br><i>Esempio</i><br>
Una persona potrebbe essere autorizzata ad entrare:
- in un orario specifico: (8-12;12:30-18:00) o all (qualsiasi orario)
- giorni specifici: Lun;Gio;Sab;Dom o all (qualsiasi giorno)
<br><br>
### Endpoints
<b>[P]</b> - endpoint pubblico
<br><b>[L]</b> - endpoint per utenti loggati
<br><b>[IC]</b> - endpoint per la comunicazione interna 
<br><b>[A]</b> - endpoint solo per admin<br><br>
- <span class='pre'>[A] | checkS</span><br>permette agli amministratori di controllare lo stato del servizio -> se tutto ok allora si riceverà un esito HTTP con status code = 200<br>
- <span class='pre'>[A] | checkSDB</span><br>permette agli amministratori di controllare se il servizio riesce ad accedere correttamente al DB -> verrà eseguita una semplice query e se risulta tutto ok allora si riceverà un esito HTTP con status code = 200<br>
- <span class='pre'>[P] | login</span><br>permette di effettuare il login
  - esito OK entro il 5° tentativo: viene ritornato un token JWT + un elenco di azioni obbligatorie (cambio pwd) + si riceverà una mail che conferma l'accesso
  - esito KO : ritorna un errore opportuno. Se si ha raggiunto il 5° tentativo errato -> l'utenza viene disabilitata per i numerosi tentativi sbagliati + si riceverà una mail di avviso<br>
- <span class='pre'>[P] | sendChangePwdLink</span><br>permette di ricevere una mail con il link per cambiare la password - Il link che si riceverà conterrà un token valido per 1gg e contenente informazioni interne (email e userId dell'utente che sta tentando di effettuare la modifica della password)<br>
- <span class='pre'>[P] | confirmOP-A1</span><br> è l'endpoint che verrà spedito via mail insieme al token per il cambio password all'utente<br> Quando l'utente aprirà questo link, verrà effettuata una validazione del token e si procederà verso la schermata di cambio password<br>
- <span class='pre'>[P] | changePwd</span><br>permette di cambiare la password agli utenti che forniscono un token JWT valido, in cui sono riportate le informazioni come email e username dell'utente che intende cambiare password. Come conferma si riceverà un token JWT aggiornato + si riceverà una mail che conferma il cambio della password<br>
- <span class='pre'>[IC] | ICRegisterUsers</span><br>richiesta proveniente dal servizio UserS solamente da utenti di tipo amministratore - registra nuovi utenti<br>
- <span class='pre'>[IC] | ICReactivateUsers</span><br>richiesta proveniente dal servizio UserS - riattiva le utenze degli utenti indicati, sia dal punto di vista del campo userDisabledPwd che userDisabled<br>
- <span class='pre'>[IC] | ICDisableUsers</span><br>richiesta proveniente dal servizio UserS - disattiva le utenze degli utenti indicati, agendo su userDisabled<br>
- <span class='pre'>[IC] | ICChangeUsrData</span><br>richiesta proveniente dal servizio UserS - permette di cambiare username, email per un utente specifico<br>
- <span class='pre'>[IC] | ICChangeUsrPwd</span><br>richiesta proveniente dal servizio UserS - permette di cambiare password per un utente specifico<br>
- <span class='pre'>[IC] | ICChangeUsersUsabilityTD</span><br>richiesta proveniente dal servizio UserS - cambia time e days riferiti alla usability degli utenti indicati<br>

### Tabelle
In questa sezione vengono descritte le tabelle gestite in questo microservizio:
- <span class='pre'>Users</span> (id, username, email, pwd, lastPwd, pwdExpired, dtPwdChanged, tokenChgPwd, dtRegistration, userDisabledPwd, userDisabled, usabilityTime, usabilityDays, token, userID_OP)<br>
  <b>Note particolari</b>:
  1. <u>lastPwd</u> è necessario per obbligare l'utente ad utilizzare una pwd diversa da quella precedente
  1. <u>pwdExpired</u> sarà un campo booleano per indicare che la password è scaduta e per obbligare l'utente a cambiarla. (Grazie a dei job automatici da far girare ogni giorno, si controllerà se è passato un mese dalla precedente modifica della password, e in tal caso si attiverà e obbligherà l'utente alla modifica della stessa non appena proverà ad effetuare il login)
  1. <u>tokenChgPwd</u> token dalla validità di 1gg, che verrà inviato via mail all'utente per consentirgli di cambiare la password
  1. <u>userDisabledPwd</u> indica se l'utente è stato disabilitato in seguito a numerosi tentativi di accesso errati
  1. <u>userDisabled</u> indica che l'utente è stato disabilitato da un amministratore o un utente autorizzato a gestire quell'utenza
  1. <u>usabilityTime</u> e usabilityDays indicano gli orari in cui quell'utente può accedere e usare il sistema
  1. <u>token</u> memorizza il token che viene emesso in fase di login. Questo dato ha una durata massima prefissata, ma se l'utente effettua l'accesso da un altro dispositivo, allora questo campo verrà sovrascritto, e il token precedente anche se ancora valido, non sarà più utilizzabile.
  1. <u>userID_OP</u> è l'id dello User che ha eseguito l'ultima operazione di creazione / modifica. Questo campo sarà presente in tutte le tabelle in cui l'utente può andare ad aggiungere / modificare i vari record.

- <span class='pre'>LogLoginActivities</span> (id, userId, loginResult, dtLogin, attemptNum, token)<br>
  <b>Note particolari</b>:
  1. <u>lastPwd</u> è necessario per obbligare l'utente ad utilizzare una pwd diversa da quella precedente
  1. <u>userDisabledPwd</u> indica se l'utente è stato disabilitato in seguito a numerosi tentativi di accesso errati
  1. <u>userDisabled</u> indica che l'utente è stato disabilitato da un amministratore o un utente autorizzato a gestire quell'utenza
  1. <u>usabilityTime</u> e usabilityDays indicano gli orari in cui quell'utente può accedere e usare il sistema
  1. <u>userID_OP</u> è l'id dello User che ha eseguito l'operazione. Questo campo sarà presente in tutte le tabelle in cui l'utente può andare ad aggiungere / modificare i vari record.