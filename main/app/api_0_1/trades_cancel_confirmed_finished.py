from flask import Response, g
from flask_restful import abort
from app.service.qrcode_service import getQRbyTempCode
import os, json
from flask_restful import Resource, marshal_with, fields
from flask_restful.reqparse import RequestParser
from app.api_0_1.common import *
from app.models.onlinetrades_dao import OnlinetradesDao, OrderEntry
from app.models.bank_trade_dao import BankTradeDao


class TradesCancelConfirmed(Resource):

	def put(self):
		parser = RequestParser(trim=True)
		parser.add_argument('trade_order', type=str, required=True, nullable=False)
		parser.add_argument('bank_order', type=str, required=True, nullable=False)
		args = parser.parse_args()
		if not args['trade_order']:
			return {'success': False, "error_msg": "订单编号错误"}
		if not args['bank_order']:
			return {'success': False, "error_msg": "银行回调编号错误"}

		onlineTrade = OnlinetradesDao.select_one_by_number(args['trade_order'])
		bankTrades = BankTradeDao.select_one_by_number(args['bank_order'])
		operator = g.current_member.username
		result = OrderEntry.insert_one_canceled_to_confirmed(onlineTrade, bankTrades, operator)
		return result


class TradesConfirmedFinished(Resource):

	def put(self):
		parser = RequestParser(trim=True)
		parser.add_argument('trade_order', type=str, required=True, nullable=False)
		parser.add_argument('bank_order', type=str, required=True, nullable=False)
		args = parser.parse_args()
		if not args['trade_order']:
			return {'success': False, "error_msg": "订单编号错误"}
		if not args['bank_order']:
			return {'success': False, "error_msg": "银行回调编号错误"}

		onlineTrade = OnlinetradesDao.select_one_by_number(args['trade_order'])
		bankTrades = BankTradeDao.select_one_by_number(args['bank_order'])
		operator = g.current_member.username
		result = OrderEntry.insert_one_confirmed_to_finished_manually(onlineTrade, bankTrades, operator)
		return result


class TradesConfirmedCancel(Resource):

	def put(self):
		parser = RequestParser(trim=True)
		parser.add_argument('trade_order', type=str, required=True, nullable=False)
		args = parser.parse_args()
		if not args['trade_order']:
			return {'success': False, "error_msg": "订单编号错误"}

		onlineTrade = OnlinetradesDao.select_one_by_number(args['trade_order'])
		operator = g.current_member.username
		result = OrderEntry.insert_one_confirmed_to_canceled(onlineTrade, operator)
		return result
