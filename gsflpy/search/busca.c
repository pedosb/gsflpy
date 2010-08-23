#include "Python.h"
#include "stdbool.h"

typedef struct node_link{
   int node;
   struct node_link *next;
}Node_link;

Node_link *new_node_link(int node){
   Node_link *nl = (Node_link*) malloc(sizeof(Node_link));
   nl->node = node;
   nl->next = NULL;
   return nl;
}

/**
 * insert the node at the end of nl
 */
void add_node(Node_link *nl, int node){
   Node_link *new_nl = (Node_link*) new_node_link(node);
   Node_link *sNl;

   for (sNl = nl; sNl->next != NULL; sNl = sNl->next);

   sNl->next = new_nl;
}

/**
 * Copy all members of a node link, but the last one.
 */
Node_link *copy_node_link(Node_link *nl){
   Node_link *new_nl = new_node_link(nl->node);
   Node_link *sNl;//searchNl
   for (sNl = nl->next; sNl != NULL; sNl = sNl->next)
      add_node(new_nl, sNl->node);
   return new_nl;
}

typedef struct sent_link{
   Node_link *nl;
   bool ready;
   int last_node;
   int node_count;
   struct sent_link *next;
}Sent_link;

Sent_link *new_sent_link(Node_link *nl){
   Sent_link *sl = (Sent_link*) malloc(sizeof(Sent_link));
   sl->nl = nl;
   sl->next = NULL;
   sl->ready = false;

   sl->node_count = 0;
   Node_link *sNl;
   for (sNl = nl; sNl->next != NULL; sNl = sNl->next)
      sl->node_count++;
   sl->last_node = sNl->node;

   return sl;
}

Sent_link *add_sent_link(Sent_link *sl, Node_link *nl){
   Sent_link *new_sl = new_sent_link(nl);
   new_sl->next = sl;
   return new_sl;
}

Sent_link *sent_link_add_node(Sent_link *sl, int node){
   sl->last_node = node;
   add_node(sl->nl, node);
   sl->node_count++;
}

int search_core(int start_node,
      int end_node,
      int nodes_lenght,
      int ***links,
      int MAX_NODES){

   int i, j,
       last_node;
   Sent_link *sl = new_sent_link(new_node_link(start_node));
   Sent_link *sSl;

   bool isPriSl;
   i = sSl->last_node;
   
   while (sSl != NULL){
      if (sSl->ready || sSl->node_count > MAX_NODES){
	 sSl = sSl->next;
	 continue;
      }

      isPriSl = true;
      last_node = sSl->last_node;

      for (j = 0; j < nodes_lenght; j++){
	 if (links[i][j] != NULL){
	    if (isPriSl){
	       isPriSl = false;
	       sent_link_add_node(sSl, j);
	    }
	    else{
	       sl = add_sent_link(sl, copy_node_link(sSl->nl));
	       sent_link_add_node(sl, j);
	    }
	 }
      }
      if (sSl->last_node == end_node)
	 sSl->ready = true;
      else
	 sSl = sl;
   }
}

int search(
