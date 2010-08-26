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
   Node_link *new_nl = new_node_link(node);
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
   for (sNl = nl->next; sNl->next != NULL; sNl = sNl->next)
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

Sent_link *new_sent_link(Node_link *nl, long int node){
   Sent_link *sl = (Sent_link*) malloc(sizeof(Sent_link));
   sl->nl = nl;
   sl->next = NULL;
   sl->ready = false;

   sl->node_count = 0;
   Node_link *sNl;
   for (sNl = nl; sNl != NULL; sNl = sNl->next)
      sl->node_count++;

   sl->last_node = node;
   return sl;
}

Sent_link *new_clear_sent_link(void){
   Sent_link *sl = (Sent_link*) malloc(sizeof(Sent_link));
   sl->nl = NULL;
   sl->next = NULL;
   sl->ready = false;
   sl->node_count = 0;
   sl->last_node = -1;

   return sl;
}

Sent_link *add_sent_link(Sent_link *sl, Node_link *nl, long int node){
   Sent_link *new_sl = new_sent_link(nl, node);
   new_sl->next = sl;
   return new_sl;
}

void sent_link_add_node(Sent_link *sl, long int link_id, long int node){
   if (sl->nl != NULL)
      add_node(sl->nl, link_id);
   else
      sl->nl = new_node_link(link_id);
   sl->last_node = node;
   sl->node_count++;
}

PyObject *
search_core(long int start_node,
      long int end_node,
      long int nodes_lenght,
      long int **links,
      long int MAX_NODES){

   //Here we consider that nodes are trasitions ids and
   //for a trasision a -> b -> c there is two trasitions
   //but we passed for 3 nodes
   MAX_NODES--;

   long int i, j;
   Sent_link *sl = NULL,
	     *sSl = NULL;

   for (j = 0; j < nodes_lenght; j++)
      if (links[start_node][j] != -1){
	 if (sl == NULL){
	    sl = new_sent_link(new_node_link(links[start_node][j]), j);
	 }else{
	    sSl = new_sent_link(new_node_link(links[start_node][j]), j);
	    sSl->next = sl;
	    sl = sSl;
	 }
      }

   sSl = sl;

   bool isPriSl,
	isMody;
   
   while (sSl != NULL){
      if (sSl->ready || sSl->node_count >= MAX_NODES){
	 sSl = sSl->next;
	 continue;
      }

      isPriSl = true;
      isMody = false;
      i = sSl->last_node;

      for (j = 0; j < nodes_lenght; j++){
	 if (links[i][j] != -1){
	    if (isPriSl){
	       isPriSl = false;
	       sent_link_add_node(sSl, links[i][j], j);
	    }
	    else{
	       isMody = true;
	       sl = add_sent_link(sl, copy_node_link(sSl->nl), j);
	       sent_link_add_node(sl, links[i][j], j);
	    }
	 }
      }
//      printf("%d end %d\n",sSl->last_node, end_node);
      if (sSl->last_node == end_node)
	 sSl->ready = true;
      if (isMody)
	 sSl = sl;
   }
//   printf("vivo\n");

   PyObject *sentList = PyList_New(0);
   PyObject *sent;
   Node_link *nl;
   for (sSl = sl; sSl != NULL; sSl = sSl->next){
      if (sSl->ready){
	 sent = PyList_New(0);
	 for (nl = sSl->nl; nl != NULL; nl = nl->next)
	    PyList_Append(sent, Py_BuildValue("l", nl->node));
	 PyList_Append(sentList, sent);
      }
   }

   return sentList; 
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

   long int **links;
   links = (long int**) malloc(sizeof(long int*) * nodes_lenght);
   for (i = 0; i < nodes_lenght; i++){
      links[i] = (long int*) malloc(sizeof(long int)*nodes_lenght);
      for (j = 0; j < nodes_lenght; j++)
	 links[i][j] = -1;
   }

   len_links_list = PyList_Size(links_list);
   for (i = 0; i < len_links_list; i++){
      link = PyList_GetItem(links_list, i);
      links[PyInt_AsLong(PyList_GetItem(link, 0))][PyInt_AsLong(PyList_GetItem(link, 1))] = i;
   }

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
   PyObject *sentences = search_core(start_node, end_node, nodes_lenght, links, MAX_NODES);
   printf("vivo\n");
   return sentences;
}

static PyObject *
gsflc_test(void){
   long int i;
   PyObject *returnList = PyList_New(0);
   for (i = 0; i < 10; i++)
      PyList_Insert(returnList, 0, Py_BuildValue("l", i));

   return returnList;
}

static PyMethodDef gsflc_methods[] = {
   {"search",  gsflc_search, METH_VARARGS,
      "Search for sentences in one graph.\n For input we expect as node the index of the in a list of node.\n the argument must be in the format:\n <start_node>,<end_node>,<number_of_nodes>,<nodes_trasition>,<max_nodes_per_sentence>\n As an example suppose the graph bellow:\n 0 \n / \\\n 1   2\n \\/\n 3\n Where 0,1,2,3 are the nodes we expect as argument:\n 0,3,4,[[0,1],[0,2],[1,3],[2,3]],10\n the return will be a list of index in the list of transitions indicating the transitions made.\n [[0,2],[1,3]]"},
   {"test", gsflc_test, METH_VARARGS,
      "document"},
   {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initgsflc(void)
{
       (void) Py_InitModule("gsflc", gsflc_methods);
}

