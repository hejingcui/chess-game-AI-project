from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self,gametiles):
        # player is always true, -> white
        # when white is at the bad side, the value is negative
        def piece_square_table_calculateb(gametiles):
            """
            Refer: https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
            Each piece has different value when in different pos.
            This evalution takes the pos of the piece into consideration as well as its value.
            :param gametiles: the gametiles
            :return: the evaluation value
            """
            PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 0, 1, 2, 3, 4, 5
            WHITE, BLACK = 0, 1
            side2move = BLACK # default is black
            WHITE_PAWN, BLACK_PAWN = 2 * PAWN + WHITE, 2 * PAWN + BLACK
            WHITE_KNIGHT, BLACK_KNIGHT = 2 * KNIGHT + WHITE, 2 * KNIGHT + BLACK
            WHITE_BISHOP, BLACK_BISHOP = 2 * BISHOP + WHITE, 2 * BISHOP + BLACK
            WHITE_ROOK, BLACK_ROOK = 2 * ROOK + WHITE, 2 * ROOK + BLACK
            WHITE_QUEEN, BLACK_QUEEN = 2 * QUEEN + WHITE, 2 * QUEEN + BLACK
            WHITE_KING, BLACK_KING = 2 * KING + WHITE, 2 * KING + BLACK
            EMPTY = BLACK_KING + 1

            def piece_to_code(piece_str):
                piece_map = {
                    "P": WHITE_PAWN,
                    "N": WHITE_KNIGHT,
                    "B": WHITE_BISHOP,
                    "R": WHITE_ROOK,
                    "Q": WHITE_QUEEN,
                    "K": WHITE_KING,
                    "p": BLACK_PAWN,
                    "n": BLACK_KNIGHT,
                    "b": BLACK_BISHOP,
                    "r": BLACK_ROOK,
                    "q": BLACK_QUEEN,
                    "k": BLACK_KING
                }
                return piece_map.get(piece_str, EMPTY)
            PCOLOR = lambda p: p & 1
            FLIP = lambda sq: sq ^ 56
            OTHER = lambda side: side ^ 1

            mg_value = [82, 337, 365, 477, 1025, 0]
            eg_value = [94, 281, 297, 512, 936, 0]

            mg_pawn_table = [
                0, 0, 0, 0, 0, 0, 0, 0,
                98, 134, 61, 95, 68, 126, 34, -11,
                -6, 7, 26, 31, 65, 56, 25, -20,
                -14, 13, 6, 21, 23, 12, 17, -23,
                -27, -2, -5, 12, 17, 6, 10, -25,
                -26, -4, -4, -10, 3, 3, 33, -12,
                -35, -1, -20, -23, -15, 24, 38, -22,
                0, 0, 0, 0, 0, 0, 0, 0,
            ]

            eg_pawn_table = [
                0, 0, 0, 0, 0, 0, 0, 0,
                178, 173, 158, 134, 147, 132, 165, 187,
                94, 100, 85, 67, 56, 53, 82, 84,
                32, 24, 13, 5, -2, 4, 17, 17,
                13, 9, -3, -7, -7, -8, 3, -1,
                4, 7, -6, 1, 0, -5, -1, -8,
                13, 8, 8, 10, 13, 0, 2, -7,
                0, 0, 0, 0, 0, 0, 0, 0,
            ]

            mg_knight_table = [
                -167, -89, -34, -49, 61, -97, -15, -107,
                -73, -41, 72, 36, 23, 62, 7, -17,
                -47, 60, 37, 65, 84, 129, 73, 44,
                -9, 17, 19, 53, 37, 69, 18, 22,
                -13, 4, 16, 13, 28, 19, 21, -8,
                -23, -9, 12, 10, 19, 17, 25, -16,
                -29, -53, -12, -3, -1, 18, -14, -19,
                -105, -21, -58, -33, -17, -28, -19, -23
            ]

            eg_knight_table = [
                -58, -38, -13, -28, -31, -27, -63, -99,
                -25, -8, -25, -2, -9, -25, -24, -52,
                -24, -20, 10, 9, -1, -9, -19, -41,
                -17, 3, 22, 22, 22, 11, 8, -18,
                -18, -6, 16, 25, 16, 17, 4, -18,
                -23, -3, -1, 15, 10, -3, -20, -22,
                -42, -20, -10, -5, -2, -20, -23, -44,
                -29, -51, -23, -15, -22, -18, -50, -64
            ]

            mg_bishop_table = [
                -29, 4, -82, -37, -25, -42, 7, -8,
                -26, 16, -18, -13, 30, 59, 18, -47,
                -16, 37, 43, 40, 35, 50, 37, -2,
                -4, 5, 19, 50, 37, 37, 7, -2,
                -6, 13, 13, 26, 34, 12, 10, 4,
                0, 15, 15, 15, 14, 27, 18, 10,
                4, 15, 16, 0, 7, 21, 33, 1,
                -33, -3, -14, -21, -13, -12, -39, -21,
            ]

            eg_bishop_table = [
                -14, -21, -11, -8, -7, -9, -17, -24,
                -8, -4, 7, -12, -3, -13, -4, -14,
                2, -8, 0, -1, -2, 6, 0, 4,
                -3, 9, 12, 9, 14, 10, 3, 2,
                -6, 3, 13, 19, 7, 10, -3, -9,
                -12, -3, 8, 10, 13, 3, -7, -15,
                -14, -18, -7, -1, 4, -9, -15, -27,
                -23, -9, -23, -5, -9, -16, -5, -17,
            ]
            mg_rook_table = [
                32, 42, 32, 51, 63, 9, 31, 43,
                27, 32, 58, 62, 80, 67, 26, 44,
                -5, 19, 26, 36, 17, 45, 61, 16,
                -24, -11, 7, 26, 24, 35, -8, -20,
                -36, -26, -12, -1, 9, -7, 6, -23,
                -45, -25, -16, -17, 3, 0, -5, -33,
                -44, -16, -20, -9, -1, 11, -6, -71,
                -19, -13, 1, 17, 16, 7, -37, -26,
            ]

            eg_rook_table = [
                13, 10, 18, 15, 12, 12, 8, 5,
                11, 13, 13, 11, -3, 3, 8, 3,
                7, 7, 7, 5, 4, -3, -5, -3,
                4, 3, 13, 1, 2, 1, -1, 2,
                3, 5, 8, 4, -5, -6, -8, -11,
                -4, 0, -5, -1, -7, -12, -8, -16,
                -6, -6, 0, 2, -9, -9, -11, -3,
                -9, 2, 3, -1, -5, -13, 4, -20,
            ]
            mg_queen_table = [
                -28, 0, 29, 12, 59, 44, 43, 45,
                -24, -39, -5, 1, -16, 57, 28, 54,
                -13, -17, 7, 8, 29, 56, 47, 57,
                -27, -27, -16, -16, -1, 17, -2, 1,
                -9, -26, -9, -10, -2, -4, 3, -3,
                -14, 2, -11, -2, -5, 2, 14, 5,
                -35, -8, 11, 2, 8, 15, -3, 1,
                -1, -18, -9, 10, -15, -25, -31, -50,
            ]

            eg_queen_table = [
                -9, 22, 22, 27, 27, 19, 10, 20,
                -17, 20, 32, 41, 58, 25, 30, 0,
                -20, 6, 9, 49, 47, 35, 19, 9,
                3, 22, 24, 45, 57, 40, 57, 36,
                -18, 28, 19, 47, 31, 34, 39, 23,
                -16, -27, 15, 6, 9, 17, 10, 5,
                -22, -23, -30, -16, -16, -23, -36, -32,
                -33, -28, -22, -43, -5, -32, -20, -41,
            ]

            mg_king_table = [
                -65, 23, 16, -15, -56, -34, 2, 13,
                29, -1, -20, -7, -8, -4, -38, -29,
                -9, 24, 2, -16, -20, 6, 22, -22,
                -17, -20, -12, -27, -30, -25, -14, -36,
                -49, -1, -27, -39, -46, -44, -33, -51,
                -14, -14, -22, -46, -44, -30, -15, -27,
                1, 7, -8, -64, -43, -16, 9, 8,
                -15, 36, 12, -54, 8, -28, 24, 14,
            ]

            eg_king_table = [
                -74, -35, -18, -18, -11, 15, 4, -17,
                -12, 17, 14, 17, 17, 38, 23, 11,
                10, 17, 23, 15, 20, 45, 44, 13,
                -8, 22, 24, 27, 26, 33, 26, 3,
                -18, -4, 21, 24, 27, 23, 9, -11,
                -19, -3, 11, 21, 23, 16, 7, -9,
                -27, -11, 4, 13, 14, 4, -5, -17,
                -53, -34, -21, -11, -28, -14, -24, -43
            ]

            mg_pesto_table = [mg_pawn_table, mg_knight_table, mg_bishop_table, mg_rook_table, mg_queen_table,
                              mg_king_table]
            eg_pesto_table = [eg_pawn_table, eg_knight_table, eg_bishop_table, eg_rook_table, eg_queen_table,
                              eg_king_table]

            gamephaseInc = [0, 0, 1, 1, 1, 1, 2, 2, 4, 4, 0, 0]
            mg_table = [[0] * 64 for _ in range(12)]
            eg_table = [[0] * 64 for _ in range(12)]

            for p, pc in zip(range(PAWN, KING + 1), range(WHITE_PAWN, BLACK_KING + 1, 2)):
                for sq in range(64):
                    mg_table[pc][sq] = mg_value[p] + mg_pesto_table[p][sq]
                    eg_table[pc][sq] = eg_value[p] + eg_pesto_table[p][sq]
                    mg_table[pc + 1][sq] = mg_value[p] + mg_pesto_table[p][FLIP(sq)]
                    eg_table[pc + 1][sq] = eg_value[p] + eg_pesto_table[p][FLIP(sq)]

            mg = [0, 0]
            eg = [0, 0]
            gamePhase = 0

            for sq in range(64):
                x = sq % 8
                y = sq // 8
                pc = gametiles[y][x].pieceonTile.tostring()
                # pc: "P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"
                # represent the piece on the square is black or white
                pc = piece_to_code(pc)
                if pc != EMPTY:
                    mg[PCOLOR(pc)] += mg_table[pc][sq]
                    eg[PCOLOR(pc)] += eg_table[pc][sq]
                    gamePhase += gamephaseInc[pc]

            mgScore = mg[side2move] - mg[OTHER(side2move)]
            egScore = eg[side2move] - eg[OTHER(side2move)]
            mgPhase = gamePhase if gamePhase <= 24 else 24
            egPhase = 24 - mgPhase
            return (mgScore * mgPhase + egScore * egPhase) // 24
        value = piece_square_table_calculateb(gametiles)
        # print(f"current value:{value}")
        return value
        # value=0
        #
        # for x in range(8):
        #     for y in range(8):
        #             if gametiles[y][x].pieceonTile.tostring()=='P':
        #                 value=value-100
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='N':
        #                 value=value-350
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='B':
        #                 value=value-350
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='R':
        #                 value=value-525
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='Q':
        #                 value=value-1000
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='K':
        #                 value=value-10000
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='p':
        #                 value=value+100
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='n':
        #                 value=value+350
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='b':
        #                 value=value+350
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='r':
        #                 value=value+525
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='q':
        #                 value=value+1000
        #
        #             if gametiles[y][x].pieceonTile.tostring()=='k':
        #
        #                value=value+10000
        # print(f"current value:{value}")
        # return value


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
