#include <stdio.h>
#include "pin.H"

FILE *trace;
ADDRINT minAddr = 0x000000000DEAD000;
ADDRINT maxAddr = 0x000000000DEAD524;

VOID printip (ADDRINT ip)
{
  if ((ip >= minAddr) && (ip <= maxAddr))
      fprintf (trace, "%p\n", (void *) ip);
}

VOID Instruction (INS ins, VOID * v)
{
  INS_InsertCall (ins, IPOINT_BEFORE, (AFUNPTR) printip, IARG_INST_PTR,
		  IARG_END);
}

VOID Fini (INT32 code, VOID * v)
{
  fprintf (trace, "#eof\n");
  fclose (trace);
}

INT32 Usage ()
{
  PIN_ERROR ("This Pintool prints the IPs of every instruction executed\n"
	     + KNOB_BASE::StringKnobSummary () + "\n");
  return -1;
}

int main (int argc, char *argv[])
{
  trace = fopen ("itrace.out", "w");
  if (PIN_Init (argc, argv))
    return Usage ();
  INS_AddInstrumentFunction (Instruction, 0);
  PIN_AddFiniFunction (Fini, 0);
  PIN_StartProgram ();
  return 0;
}  
