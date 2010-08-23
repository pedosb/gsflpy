#include "Python.h"
#include "stdbool.h"

typedef struct node_link{
   long int node;
   struct node_link *next;
}Node_link;

Node_link *new_node_link(long int node){
   Node_link *nl = (Node_link*) malloc(sizeof(Node_link));
   nl->node = node;
   nl->next = NULL;
   return nl;
}

/**
 * insert the node at the end of nl
 */
void add_node(Node_link *nl, long int node){
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
   long int last_node;
   long int node_count;
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

void sent_link_add_node(Sent_link *sl, long int node){
   sl->last_node = node;
   add_node(sl->nl, node);
   sl->node_count++;
}

long int search_core(long int start_node,
      long int end_node,
      long int nodes_lenght,
      bool **links,
      long int MAX_NODES){

   long int i, j,
       last_node;
   Sent_link *sl = new_sent_link(new_node_link(start_node));
   Sent_link *sSl = sl;

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
	 if (links[i][j] == true){
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
   return 1;
}

static PyObject *
gsflc_search(PyObject *self, PyObject * args){
   long int i, j,
	len_links_list;
   long int start_node,
	end_node,
	nodes_lenght,
	MAX_NODES;

   PyObject *links_list;
   PyObject *link;

   PyArg_ParseTuple(args, "lllOl",
	 &start_node,
	 &end_node,
	 &nodes_lenght,
	 &links_list,
	 &MAX_NODES);

   bool **links;
   links = (bool**) malloc(sizeof(bool*) * nodes_lenght);
   for (i = 0; i < nodes_lenght; i++){
      links[i] = (bool*) malloc(sizeof(bool)*nodes_lenght);
      for (j = 0; j < nodes_lenght; j++)
	 links[i][j] = false;
   }

   len_links_list = PyList_Size(links_list);
   for (i = 0; i < len_links_list; i++){
      link = PyList_GetItem(links_list, i);
      links[PyInt_AsLong(PyList_GetItem(link, 0))][PyInt_AsLong(PyList_GetItem(link, 1))] = true;
   }

#define _DEBUG
#ifdef _DEBUG
   printf("Start %d\nEnd %d\nLen %d\nMax %d\n",
	 start_node,
	 end_node,
	 nodes_lenght,
	 MAX_NODES);
   for (i = 0; i < nodes_lenght; i++){
      for (j = 0; j < nodes_lenght; j++)
	 printf("%d ", links[i][j]);
      printf("\n");
   }
#endif

   search_core(start_node, end_node, nodes_lenght, links, MAX_NODES);

   PyObject *returnList = PyList_New(10);
   for (i = 0; i < 10; i++)
      PyList_SetItem(returnList, i, Py_BuildValue("l", i));

   return returnList;
}

static PyMethodDef gsflc_methods[] = {
   {"search",  gsflc_search, METH_VARARGS,
      "Searc for sentences in the graph."},
   {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initgsflc(void)
{
       (void) Py_InitModule("gsflc", gsflc_methods);
}

