import numpy as np

def gram_schmidt(A):
    """Gram-schmidt"""
    Q=np.zeros_like(A)
    cnt = 0
    for a in A.T:
        u = np.copy(a)
        for i in range(0, cnt):
            u -= np.dot(np.dot(Q[:, i].T, a), Q[:, i]) #
        e = u / np.linalg.norm(u)
        Q[:, cnt] = e
        cnt += 1
    R = np.dot(Q.T, A)
    return (Q, R)

def givens_rotation(A):
    """Givens"""
    (r, c) = np.shape(A)
    Q = np.identity(r)
    R = np.copy(A)
    (rows, cols) = np.tril_indices(r, -1, c)
    for (row, col) in zip(rows, cols):
        if R[row, col] != 0:
            r_ = np.hypot(R[col, col], R[row, col])  # d
            c = R[col, col]/r_
            s = -R[row, col]/r_
            G = np.identity(r)
            G[[col, row], [col, row]] = c
            G[row, col] = s
            G[col, row] = -s
            R = np.dot(G, R)  # R=G(n-1,n)*...*G(2n)*...*G(23,1n)*...*G(12)*A
            Q = np.dot(Q, G.T)  # Q=G(n-1,n).T*...*G(2n).T*...*G(23,1n).T*...*G(12).T
    return (Q, R)

def householder_reflection(A):
     """Householder"""
     (r, c) = np.shape(A)
     Q = np.identity(r)
     R = np.copy(A)
     for cnt in range(r - 1):
         x = R[cnt:, cnt]
         e = np.zeros_like(x)
         e[0] = np.linalg.norm(x)
         u = x - e
         v = u / np.linalg.norm(u)
         Q_cnt = np.identity(r)
         Q_cnt[cnt:, cnt:] -= 2.0 * np.outer(v, v)
         R = np.dot(Q_cnt, R)
         Q = np.dot(Q, Q_cnt)
     return (Q, R)

np.set_printoptions(precision=4, suppress=True)
A = np.array([[6, 5, 0],[5, -1, 4],[5, 1, -14],[0, 4, 3]],dtype=float)
(Q, R) = gram_schmidt(A)
print(Q)
print(R)
print np.dot(Q,R)

(Q, R) = givens_rotation(A)
print(Q)
print(R)
print np.dot(Q,R)

(Q, R) = householder_reflection(A)
print(Q)
print(R)
print np.dot(Q,R)