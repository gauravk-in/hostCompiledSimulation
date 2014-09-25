/**
 * Called when a new branch is entered.
 *
 * name: string containing name of the basic block.
 * blockObjStartAdd : Starting address of basic block from objdump
 * blockObjEndAdd : End address of basic block from objdump
 *
 * returns whether branch was predicted or not
 */
extern unsigned int enterBlock (unsigned long blockObjStartAdd,
		unsigned long blockObjEndAdd);


extern void branchPred_init();
