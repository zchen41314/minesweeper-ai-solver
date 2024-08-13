// ======================================================================
// FILE:        MyAI.cpp
//
// AUTHOR:      Jian Li
//
// DESCRIPTION: This file contains your agent class, which you will
//              implement. You are responsible for implementing the
//              'getAction' function and any helper methods you feel you
//              need.
//
// NOTES:       - If you are having trouble understanding how the shell
//                works, look at the other parts of the code, as well as
//                the documentation.
//
//              - You are only allowed to make changes to this portion of
//                the code. Any changes to other portions of the code will
//                be lost when the tournament runs your code.
// ======================================================================

#include "MyAI.hpp"

MyAI::MyAI ( int _rowDimension, int _colDimension, int _totalMines, int _agentX, int _agentY ) : Agent()
{
    // ======================================================================
    // YOUR CODE BEGINS
    // ======================================================================
    rowDimension = _rowDimension;
    colDimension = _colDimension;
    totalMines = _totalMines;
    agentX = _agentX;
    agentY = _agentY;
    amountOfCoveredTiles = rowDimension * colDimension;
    previousMove = {UNCOVER, agentX, agentY};

    // resizing my mine sweeper board vector to the board size
    myMineSweeperBoard.resize(rowDimension);
    for (int i = 0; i < colDimension; i++) {
        myMineSweeperBoard[i].resize(colDimension);
    }

    // initializing my board to C meaning tile is covered
    for (int i = 0; i < rowDimension; i++) {
        for (int j = 0; j < colDimension; j++) {
            myMineSweeperBoard[i][j] = 'C';
        }
    }

    myFrontier.resize(colDimension);
    for (int i = 0; i < rowDimension; i++) {
        myFrontier[i].resize(rowDimension);
    }

    // initializing my board to C meaning tile is covered
    for (int i = 0; i < rowDimension; i++) {
        for (int j = 0; j < colDimension; j++) {
            myFrontier[i][j] = 'X';
        }
    }

    // U means uncovered
    myMineSweeperBoard[rowDimension - agentY][agentX - 1] = 'U';
    amountOfCoveredTiles = amountOfCoveredTiles - 1;
    // ======================================================================
    // YOUR CODE ENDS
    // ======================================================================
};


// returns the action, x coordinate, y coordinate
Agent::Action MyAI::getAction( int number )
{
    // ======================================================================
    // YOUR CODE BEGINS
    // ======================================================================
    if (amountOfCoveredTiles == totalMines) {
        return {LEAVE,-1,-1};
    } 

    if (number == 0) {
        
        return {UNCOVER, previousMove.x - 1};
    }
 {

 }
    return {LEAVE,-1,-1};
    // ======================================================================
    // YOUR CODE ENDS
    // ======================================================================

}


// ======================================================================
// YOUR CODE BEGINS
// ======================================================================



// ======================================================================
// YOUR CODE ENDS
// ======================================================================
