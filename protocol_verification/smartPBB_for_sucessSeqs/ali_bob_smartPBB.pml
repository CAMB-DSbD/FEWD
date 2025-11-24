/*
 *  ali_bob_smartPBB.pml 
 *  a Promela model of synchronisation operation of the
 *  FEWD fair exchange protocol, using a smart contract
 *  deployed on a blockchain.
 *  
 *  It models a syncronisation protocol that Alice's application
 *  and Bob's application use to synchronise with each other
 *  the next local states to either: YES or NO.
 *
 *  Inspiration:
 *  http://spinroot.com/spin/Man/Exercises.html
 *
 *  It has been implemented to validate the FEWD protocol
 *  described in the book
 *  "Fair Exchange: Theory and Practice of Digital Belongings"
 *  Carlos Molina-Jimenez et al. 
 *  https://www.worldscientific.com/worldscibooks/10.1142/q0448
 *  
 *  It includes three processes and the spin init process.
 *  smartPBB: the smart contract-based Public Boulletin Board
 *  ali: Ali's application
 *  bob: Bob's application.
 *
 *  Programmer: Carlos Molina Jimenez (carlos.molina@cl.cam.ac.uk)
 *              Computer Lab; University of Cambridge
 * 
 *  Date: 4 Jul 2025
 *  Last alteration date: 5 Jul 2025
 *
 *
 * Execution environment: 
 * 1) I have tested it in Spin Version 6.5.2 -- 6 December 2019
 * 2) I have a MacBook Pro: Apple M2 Pro, 16 GB, Ventura 13.5.2
 * 3) I installed Spin following
 *    https://gist.github.com/leo-pfeiffer/92a095fa92d247fb9a788fbe9c84b2a6
 *    
 * To continue the examination of the model, the reader migh like
 * to have a look at Gerard's book
 * Spin Model Checker, The: Primer and Reference Manual 
 * By Gerard J. Holzmann
 * https://www.cin.ufpe.br/~acm/esd/intranet/spinPrimer.pdf
 *
 * iSpin is a graphical interface to spin, see
 * a) http://spinroot.com/spin/Man/3_SpinGUI.html
 * b) Installation process and main functionalities of the Spin model checker
 *    Miguel J. Hornos and Juan Carlos Augusto
 *
 * I have tested:  https://spinroot.com/spin/Man/Manual.html
 * 1) Show msgs send and received
 * carlos@fewd% spin -sr ali_bob_smartPBB.pml
 *
 * 2) spin -n100 -r ali_bob_smartPBB.pml | grep "proc  2"
 *
 * 
 */


 /* ****  How to generate the sequences (5Jul2025) *****
 
 01) Include the bool vars in the promela mode: s,c

 02) Set s and c to  false

 03) carlos@fewd% spin -f "!(<>s)"  to generate the never claim.

 04) Copy and paste the generated code to the promela
    model, eg ali_bob_smartPBB.pml

 05) carlos@fewd% spin -a ali_bob_smartPBB.pml  to generate pan.c

 06) carlos@fewd% cc -o pan pan.c  to generate pan

 07) carlos@fewd% pan -a -e -c500 ali_bob_smartPBB.pml
    to generate 500 trail files max
    The model will output 
    ali_bob_smartPBB.pml1.trail
    ali_bob_smartPBB.pml2.trail
    ali_bob_smartPBB.pml3.trail
    etc.
    ali_bob_smartPBB.pml500.trail
    
    Since I have #define MAX_NUM_TOKENS 8  
    The model produces thousands of trial files. The size of the
    files can help to identify the two files with the
    sequences acc_ali | acc_bob and acc_bob | acc_ali 

    Use % ls -S -l *.trail
        to sort the trail files by size
 
 08) To examine the tokens involded in ali_bob_smartPBB.pml1.trail run
     carlos@fewd% spin -t1 -r -B ali_bob_smartPBB.pml
    
 09) To examine the tokens involded in ali_bob_smartPBB.pml2.trail run
     carlos@fewd% spin -t2 -r -B ali_bob_smartPBB.pml

 10) To examine the tokens involded in ali_bob_smartPBB.pml3.trail run
     carlos@fewd% spin -t3 -r -B ali_bob_smartPBB.pml

    t1 refers to the number of the trial file: 1, 2,..., 500 
    r  means r(eceived), eg, the msg (tokens in our exa) received
       by smartPBB. 
    B  I dont remember 

 11) carlos@fewd% spin -t1 -r -B ali_bob_smartPBB.pml | fgrep "<token>"
     To see the sequence of tokens received ali_bob_smartPBB.pml1.trail

 12) I can do the same with other trials


 13) To reduce the number of trail files 
     set #define MAX_NUM_TOKENS 2
     It generates only about 100 trail files.

  See
  /Users/carlosmolina/papers/newcastle_papers/cbi2013Vienna/BuyerStoreContractForPaperEPROMELA/ContWithLTLforSeqWithoutXML
  This is a local file, its is not online yet. I can provide it upon request

 
  See also
  https://github.com/carlos-molina/contraval/blob/master/examples/helloWorldSmartContractInitOrTO/pro2seq 
  pro2seq is a linux shell that can be used to automate the process
  of generating the sequences and srtoring them in xml-style.
  The xml-style sequences can be used as input programmatically to the 
  implementation under test (the FEWD protocol). 
  
 */


#define s (succ==true)  /* used by the LTL formula */
#define c (canc==true)  

bool succ= false;  /* used by the LTL formula */
bool canc= false;



#define MAX_NUM_TOKENS 8 /* max number of tokens that Ali or Bob are */ 
                         /* allowed to post to the PBB               */

mtype = {acc_ali, rej_ali, acc_bob, rej_bob}; /* four types of tokens    */ 

chan cha=[0] of {mtype}; /* Randevous channel (0 slots)   used by  */


/*
 * smartPBB
 * models a smart contract deployed on a blockchain.
 * It models a FSM with five states, including two
 * final states: sucess and cancel.
 * State transitions are determined by the arrival of 
 * four tokens posted by ali and bob:
 * ali: acc_ali and rej_ali
 * bob: acc_bob and rej_bob 
 *
 * acc and rej stand for accept and reject, respectively.
 * ali posts acc_ali when she wishes to reach the
 * success final state.
 * ali posts rej_ali when she wishes to reach the sucess
 * final state.
 * Bob operates similarly, except that he posts acc_bob 
 * and rej_bob, respectively.
 */
proctype smartPBB() 
{
 mtype token; /* token received from ali and bob */

 S_init: cha ? token ->
         printf("\n<token>%e</token>\n\n",token);
         if
         :: token == acc_ali -> goto S_ali_wish2exc
         :: token == rej_ali -> goto End_S_cancel
         :: token == acc_bob -> goto S_bob_wish2exc
         :: token == rej_bob -> goto End_S_cancel
         fi; 


 S_ali_wish2exc: cha ? token ->
         printf("\n<token>%e</token>\n\n",token);
         do 
         :: token == acc_ali -> goto S_ali_wish2exc 
         :: token == rej_ali -> goto End_S_cancel
         :: token == acc_bob -> goto End_S_success
         :: token == rej_bob -> goto End_S_cancel
         od;


 S_bob_wish2exc: cha ? token ->
         printf("\n<token>%e</token>\n\n",token);
         do 
         :: token == acc_ali -> goto End_S_success
         :: token == rej_ali -> goto End_S_cancel
         :: token == acc_bob -> goto S_bob_wish2exc 
         :: token == rej_bob -> goto End_S_cancel
         od;

 End_S_success: 
         printf("\nsmartPBB in final state: End_S_success\n");
         succ=true;  /* var s used in LTL becomes true in this state */ 
         cha ? token ->
         printf("\n<token>%e</token>\n\n",token);
         do 
         :: token == acc_ali -> goto End_S_success
         :: token == rej_ali -> goto End_S_success
         :: token == acc_bob -> goto End_S_success
         :: token == rej_bob -> goto End_S_success
         od;


 End_S_cancel: 
         printf("\nsmartPBB in final state: End_S_cancel\n");
         canc=true;   /* var c used in LTL becomes true in this state */ 
         cha ? token ->
         printf("\n<token>%e</token>\n\n",token);
         do 
         :: token == acc_ali -> goto End_S_cancel
         :: token == rej_ali -> goto End_S_cancel
         :: token == acc_bob -> goto End_S_cancel
         :: token == rej_bob -> goto End_S_cancel
         od 
}



/*
 * ali:
 * models Alice's application:
 * Posts two types of tokens to the smartPBB:
 * acc_ali: Alice's applications wishes to synchronise with 
 *          Bob's application.
 * rej_ali: Alice's applications wishes to cancel.
 */
proctype ali()
{
 mtype token;                   /* token to post to smartPBB          */
 byte num_tokens=0;      /* counts num of token posted by appa */

 do
 :: num_tokens< MAX_NUM_TOKENS ->
    if
    :: token= acc_ali 
    :: token= rej_ali
    fi;
    cha ! token;
    num_tokens++
 :: num_tokens >= MAX_NUM_TOKENS -> break
 od;
 printf("\n   ===>>> Ali ended");
 printf(" num_token= %d",num_tokens)
}


/*
 * bob:
 * models Bob's application:
 * Posts two types of tokens to the smartPBB:
 * acc_bob: Bob's applications wishes to synchronise with 
 *          Alice's application.
 * rej_bob: Bob's applications wishes to cancel.
 */
proctype bob()
{
 mtype token;        /* token to post to smartPBB          */
 byte num_tokens=0;  /* counts num of token posted by appa */
                     /* it this ver, it is set to 4        */

 do
 :: num_tokens< MAX_NUM_TOKENS ->
    if
    :: token= acc_bob 
    :: token= rej_bob
    fi;
    cha ! token;
    num_tokens++
 :: num_tokens >= MAX_NUM_TOKENS -> break
 od;
 printf("\n   ===>>> Bob ended");
 printf(" num_token= %d",num_tokens)
}



/*
 * spin init process:
 * It initiates single instances of the PBB, ali and bob 
 */
init {
  run smartPBB();
  run ali();
  run bob()
}



/*
 * Use spin to generate a claim that the pan model never 
 * reaches the state where s becomes true: 
 *
 * carlos@fewd% spin -f "<>s"
 *
 * and copy and paste the output here.
 *
 * Since the model can reach such a state, the
 * model outputs counterexamples (N trial files)
 * with the sequences of tokens that lead from the
 * initial state to that state where s becomes true.
 */
never  {    /* <>s */
T0_init:
	do
	:: atomic { ((s)) -> assert(!((s))) }
	:: (1) -> goto T0_init
	od;
accept_all:
	skip
}



/*
 * If I  wish to test that the state where c becomes true
 * is reachable, I can use spin similarly to generate:

carlos@fewd% spin -f "<>c"
never  {     
T0_init:
	do
	:: atomic { ((c)) -> assert(!((c))) }
	:: (1) -> goto T0_init
	od;
accept_all:
	skip
}

 * and copy and paste it here and delete the TLT for testing
 * s: only a single LTL c an be verified at a time by spin.
 *
 */

