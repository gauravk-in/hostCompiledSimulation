#ifndef SHA_H
#define SHA_H

/* NIST Secure Hash Algorithm */
/* heavily modified from Peter C. Gutmann's implementation */

/* Useful defines & typedefs */

typedef unsigned char BYTE;
typedef unsigned long LONG;

#define SHA_BLOCKSIZE		64
#define SHA_DIGESTSIZE		20

struct SHA_INFO {
    unsigned long digest[5];		/* message digest */
    unsigned long count_lo, count_hi;	/* 64-bit bit count */
    unsigned long data[16];		/* SHA data buffer */
};

void sha_init(struct SHA_INFO *);
void sha_update(struct SHA_INFO *, unsigned char *, int);
void sha_final(struct SHA_INFO *);

void sha_stream(struct SHA_INFO *, unsigned char *, unsigned long);
void sha_print(struct SHA_INFO *);

#endif /* SHA_H */
