/* 
 * helloworld.pml
 * shows the basic concept of a Promela
 * program.
 * An process called alice sends a greeting message
 * to a process called bob, over a channel. 
 *
 * Programmer:
 * Carlos Molina-Jimenez (carlos.molina@cl.cam.ac.uk)
 * Departmet of Computer Science and Technology
 * University of Cambridge
 *
 * 23 sep 2025
 *
 * To run a random simulation of the model
 * https://spinroot.com/spin/Man/Spin.html
 *
 * % spin -s -r helloworld.pml
 * 4:	proc  0 (alice:1) helloworld.pml:24 Sent hello	-> queue 1 (ch_a2b)
 * 4:	proc  4 (bob:1) helloworld.pml:35 Recv hello	<- queue 1 (ch_a2b)
 *
 */

mtype= {hello};              /* msg to send to bob   */
chan ch_a2b= [0] of {mtype}; /* channel alice to bob */


/*
 * alice process sends (!) a msg to bob process.
 * a and b stand for alice and bob
 */
active proctype alice()
 {
  mtype msg_to_b;  /* msg to bob */

  msg_to_b= hello;

  ch_a2b ! msg_to_b
 }


/*
 * bob process waits (?) to receive a msg from alice
 * a and b stand for alice and bob
 */
active proctype bob()
 {
  mtype msg_from_a; /* msg from alice */

  ch_a2b ? msg_from_a;

  printf("\n bob recvd from alice msg: %e\n", msg_from_a) 
 }


/*
 * spin init process:
 * It initiates single instances of ali and bob 
 */
init 
{
  run alice();
  run bob()
}

